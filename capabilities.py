#!/usr/bin/env python3
"""Offline materializer/validator for portable role capability payloads.

This is source packaging, not a runtime installer. Normal Hermes profile
installation remains the only installation path; no downloads/auth/subprocesses.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
NARROW = {'hermes-wear', 'agency-orchestrator', 'academy-dean', 'council-steward'}
GUIDE = 'skills/capabilities/profile-capabilities'
SHA = re.compile(r'^[0-9a-f]{40}$')


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def json_text(value) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + '\n'


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_profiles(root: Path) -> dict[str, str]:
    result = {}
    for pack in load_json(root / 'packs.json')['packs']:
        for row in load_json(root / pack['manifest'])['profiles']:
            if row['name'] in result:
                raise ValueError('duplicate roster identity: ' + row['name'])
            result[row['name']] = str(Path(pack['path']) / 'profiles' / row['name'])
    result['hermes-wear'] = 'hermes-wear'
    return result


def render_outputs(root: Path, data: dict) -> dict[Path, bytes]:
    """Validate exact selections before rendering ANY output (fail closed)."""
    records = data['profiles']
    names = [r['profile'] for r in records]
    expected = source_profiles(root)
    if len(names) != len(set(names)) or set(names) != set(expected):
        raise ValueError('capability identities do not exactly match public source rosters + Wear')
    lock = load_json(root / 'capabilities/skills.lock.json')['skills']
    integrations = load_json(root / 'capabilities/integrations.json')
    outputs = {}
    table = ['# Complete capability matrix', '',
             'Every public profile is included. Supplemental skills are shipped on demand; all external integrations are disabled opt-ins. Existing role-owned jobs remain unchanged.', '',
             '| Profile | Supplemental skills | Optional plugins | Optional MCPs |',
             '|---|---|---|---|']
    csv_buffer = io.StringIO(newline='')
    writer = csv.writer(csv_buffer, lineterminator='\n')
    writer.writerow(['profile', 'pack', 'skills', 'plugins', 'mcps', 'decision'])
    for name, record in lock.items():
        if not SHA.fullmatch(record['commit']):
            raise ValueError('unresolved skill pin: ' + name)
        tree = root / 'capabilities/skills' / name
        actual = {str(p.relative_to(tree)): file_hash(p) for p in tree.rglob('*')
                  if p.is_file() and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts and p.suffix != '.pyc'}
        if actual != record['files'] or not (tree / 'LICENSE').is_file():
            raise ValueError('canonical skill hash/license drift: ' + name)
    for row in records:
        name = row['profile']
        if row['path'] != expected[name]:
            raise ValueError('profile source path drift: ' + name)
        target = root / row['path']
        actual_owned = sorted(p.parent.name for p in (target / 'skills').glob('*/SKILL.md'))
        if actual_owned != row['existing_skills']:
            raise ValueError('role-owned skill drift: ' + name)
        if (target / '.no-bundled-skills').exists() != row['bundled_skills_opt_out']:
            raise ValueError('bundled skill opt-out drift: ' + name)
        if name in NARROW and any(row[k] for k in ('skills', 'plugins', 'mcps')):
            raise ValueError('narrow profile execution expansion: ' + name)
        for kind in ('skills', 'plugins', 'mcps'):
            ids = [i['name'] for i in row[kind]]
            if len(ids) != len(set(ids)):
                raise ValueError('duplicate selection: ' + name + '/' + kind)
        for selected in row['skills']:
            skill = selected['name']
            if skill not in lock or skill in row['existing_skills']:
                raise ValueError('unreviewed or duplicate skill: ' + name + '/' + skill)
            src = root / 'capabilities/skills' / skill
            destination = Path(lock[skill]['install_path'])
            for rel in lock[skill]['files']:
                outputs[target / destination / rel] = (src / rel).read_bytes()
        for shadow in row.get('seed_shadows', []):
            if shadow['name'] not in row['existing_skills']:
                raise ValueError('seeding shadow must preserve a role-owned skill: ' + name)
            source = target / shadow['source']
            destination = target / shadow['destination']
            if not shadow['destination'].startswith('skills/') or source == destination:
                raise ValueError('invalid seeding shadow destination: ' + name)
            for item in source.rglob('*'):
                if item.is_file() and '__pycache__' not in item.parts and item.suffix != '.pyc':
                    outputs[destination / item.relative_to(source)] = item.read_bytes()
        catalog = {'profile': name, 'role': row['role'], 'reason': row['reason'],
                   'skills': row['skills'], 'plugins': [], 'mcps': [],
                   'seed_shadows': row.get('seed_shadows', [])}
        for kind in ('plugins', 'mcps'):
            for selected in row[kind]:
                item = integrations[kind].get(selected['name'])
                if item is None:
                    raise ValueError('unreviewed integration: ' + selected['name'])
                item = {**item, 'reason': selected['reason']}
                if kind == 'plugins':
                    if not SHA.fullmatch(item['commit']):
                        raise ValueError('plugin requires immutable pin: ' + item['name'])
                    item['install_command'] = ['hermes', '-p', name, 'plugins', 'install', item['identifier'],
                                               '--ref', item['commit'], '--no-enable', '--no-deps']
                else:
                    cfg = item['config']
                    if cfg.get('enabled') is not False or cfg.get('sampling', {}).get('enabled') is not False:
                        raise ValueError('integration auto-activation/sampling: ' + item['name'])
                    if item.get('transport') == 'local-stdio':
                        expected_entrypoints = {
                            'pixelorama': '<pixelorama-mcp-checkout>/mcp-server/dist/index.js',
                            'aseprite': '<aseprite-mcp-checkout>/build/index.js',
                        }
                        entrypoint = expected_entrypoints.get(item['name'])
                        tools = cfg.get('tools', {})
                        allowlist = tools.get('include')
                        patch = target / item['setup_patch']
                        if (not patch.is_file() or file_hash(patch) != item['setup_patch_sha256']
                                or not entrypoint or not SHA.fullmatch(item.get('commit', ''))
                                or cfg.get('command') != 'node' or cfg.get('args') != [entrypoint]
                                or 'url' in cfg or cfg.get('env') or cfg.get('cwd')
                                or cfg.get('trust') != 'untrusted'
                                or cfg.get('elicitation', {}).get('enabled') is not False
                                or cfg.get('supports_parallel_tool_calls') is not False
                                or tools.get('resources') is not False or tools.get('prompts') is not False
                                or not isinstance(allowlist, list) or not allowlist
                                or any(not isinstance(tool, str) or not re.fullmatch(r'[a-z][a-z0-9_]*', tool)
                                       for tool in allowlist)
                                or set(allowlist).intersection(item['required_tool_exclusions'])):
                            raise ValueError('invalid reviewed local MCP template: ' + item['name'])
                    elif not str(cfg.get('url', '')).startswith('https://') or 'command' in cfg:
                        raise ValueError('invalid reviewed HTTPS MCP template: ' + item['name'])
                    if cfg.get('headers') or cfg.get('env'):
                        raise ValueError('credential-bearing MCP seed: ' + item['name'])
                catalog[kind].append(item)
        guide = target / GUIDE
        outputs[guide / 'references/catalog.json'] = json_text(catalog).encode()
        if row['mcps']:
            seed = {'mcp_servers': {m['name']: m['config'] for m in catalog['mcps']}}
            outputs[guide / 'references/mcp-servers.json'] = json_text(seed).encode()
            # Valid JSON is valid YAML; supported Hermes fresh-install config seed.
            # Updates preserve the recipient's config.yaml unless they deliberately reset it.
            if row.get('config_seed', False):
                outputs[target / 'config.yaml'] = json_text(seed).encode()
        if row['plugins']:
            pack = {'name': name + '-integrations', 'version': '1.0.0',
                    'description': 'Optional reviewed integrations; never installed automatically.',
                    'plugins': [{'repo': p['repository'], 'subdir': p['subdir'], 'ref': p['commit']} for p in catalog['plugins']]}
            outputs[guide / 'references/hermes-pack.yaml'] = json_text(pack).encode()
        skill_list = '\n'.join('- `' + s['name'] + '`: ' + s['reason'] for s in row['skills']) or '- No additional execution skill: existing specialist workflows already cover this scope.'
        skill = f'''---
name: profile-capabilities
description: "Use when discovering this profile's skills or optional integrations."
version: 1.0.0
author: Hermes Profile Packs contributors
license: AGPL-3.0-only
---

# Capabilities for {name}

{row['role']}

## Role-specific selection

{row['reason']}

{skill_list}

## Procedure

1. Prefer the existing role-owned workflow and native Hermes tools. Load one matching supplemental skill on demand with `skill_view`; never preload the whole catalog or duplicate a capability via a connector and MCP.
2. Read `references/catalog.json` with `skill_view(name="profile-capabilities", file_path="references/catalog.json")` for exact optional integration pins, prerequisites, privacy/egress disclosures, setup and fallback decisions. A listed integration is not an installed or authenticated integration.
3. All external plugins/MCPs are explicit opt-ins. Do not connect, download, launch, authenticate, schedule, upload records/code, or change live configuration merely because a profile was installed. Even anonymous hosted services disclose queries. Native read/search/file/browser tools remain the fallback when available and authorized.
4. If the user chooses an integration, inspect current `hermes` CLI help, exact profile identity, existing connectors and enabled state. Obtain consent for the named service, transmitted data, costs and permissions. Use supported Hermes UI/CLI; never edit live YAML, bypass TLS, ask for secrets in chat, or copy credentials between profiles.
5. Plugin commands in the catalog stage reviewed code disabled without dependency installation. Review current capability and dependency consent before a separate enable action. Warning: native `plugins pack install` enables plugins; `references/hermes-pack.yaml`, if present, is an explicit activation recipe, NOT disabled staging. Use the individual `--no-enable --no-deps` catalog commands for staging, and never invoke pack install during profile provisioning.
6. Fresh installs may contain disabled MCP config seeds. Existing-profile updates preserve user config: compare `references/mcp-servers.json` when present and use supported MCP setup only after approval. Do not reset the whole config or overwrite existing accounts. MCP sampling is disabled; pruning/allowlisting tools and provider authentication are separate decisions.
7. Read back exact enabled state and tools after any approved change. Test a non-sensitive read. Report credential/setup/network failures honestly; do not pretend a failed lookup returned no data. Account for reload/new-session effects; never restart a gateway implicitly.
8. Preserve user customizations. Native distribution updates replace shipped skill roots, but unrelated skill roots survive. Review same-name local collisions before updating; do not claim user-edited shipped skills are protected. Rollback is a reviewed source revision plus a separate approved installed-state restore, never deleting all skills or secrets.

## Boundaries

Installing this pack does not widen role authority or tool permissions. Council retains minimum-necessary personal context and professional-advice boundaries. Academy retains teaching, assessment and CE routing contracts. Coordination profiles remain coordination-only. Wear must keep wrist-first output, device capability verification, backend approvals, and its disabled execution toolsets; unavailable device tools mean no action, not invented success.
'''
        outputs[guide / 'SKILL.md'] = skill.encode()
        values = [name, ', '.join(s['name'] for s in row['skills']) or 'retain only',
                  ', '.join(s['name'] for s in row['plugins']) or 'none',
                  ', '.join(s['name'] for s in row['mcps']) or 'none']
        table.append('| ' + ' | '.join(values) + ' |')
        writer.writerow([name, row['pack'], values[1], values[2], values[3], row['reason']])
    outputs[root / 'docs/CAPABILITY_MATRIX.md'] = ('\n'.join(table) + '\n').encode()
    outputs[root / 'capabilities/matrix.csv'] = csv_buffer.getvalue().encode()
    return outputs


def run(root: Path = ROOT, *, check: bool = True) -> list[str]:
    data = load_json(root / 'capabilities/profiles.json')
    outputs = render_outputs(root, data)
    errors = []
    baseline = load_json(root / 'capabilities/baseline.json')['profile_source_files']
    for relative, digest in baseline.items():
        path = root / relative
        if not path.is_file() or file_hash(path) != digest:
            errors.append('original profile functionality changed: ' + relative)
    for row in data['profiles']:
        for index in (root / row['path'] / 'skills').rglob('SKILL.md'):
            text = index.read_text(encoding='utf-8')
            header = text.split('---', 2)[1] if text.startswith('---') else ''
            match = re.search(r'^name:\s*[\"\']?([a-z0-9-]+)[\"\']?\s*$', header, re.M)
            if index.is_symlink() or not match or match[1] != index.parent.name:
                errors.append('skill identity/symlink violation: ' + str(index.relative_to(root)))
    if errors:
        return errors  # Never regenerate over drift in original authored source.
    for path, content in outputs.items():
        if check:
            if not path.is_file() or path.read_bytes() != content:
                errors.append('missing/stale generated artifact: ' + str(path.relative_to(root)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    for row in data['profiles']:
        bases = [p for p in (root / row['path'] / 'skills').iterdir()
                 if p.is_dir() and p.name not in row['existing_skills']]
        actual = {p for base in bases for p in base.rglob('*')
                  if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}
        extra = actual - set(outputs)
        errors.extend('unexpected supplemental file: ' + str(p.relative_to(root)) for p in sorted(extra))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='read-only drift and safety validation (default)')
    parser.add_argument('--write', action='store_true', help='materialize source artifacts offline; never touches installed profiles')
    args = parser.parse_args()
    if args.check and args.write:
        parser.error('choose --check or --write')
    try:
        errors = run(check=not args.write)
    except (ValueError, KeyError, OSError) as exc:
        print('Capability validation failed: ' + str(exc), file=sys.stderr)
        return 1
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    data = load_json(ROOT / 'capabilities/profiles.json')['profiles']
    print(json_text({'status': 'PASS', 'profiles': len(data), 'by_pack': dict(Counter(r['pack'] for r in data)),
                     'supplemental_skill_assignments': sum(len(r['skills']) for r in data),
                     'plugin_opt_ins': sum(len(r['plugins']) for r in data),
                     'mcp_opt_ins': sum(len(r['mcps']) for r in data)}), end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
