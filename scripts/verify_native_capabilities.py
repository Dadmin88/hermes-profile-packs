#!/usr/bin/env python3
"""Offline native distribution proof. Run with an authorized Hermes source interpreter.

Only a newly-created disposable directory is used. No accounts, secrets,
providers, production profiles, aliases, gateways or external services.
"""
from pathlib import Path
import argparse
import json
import os
import socket
import sys
import tempfile
from unittest.mock import patch


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--hermes-source',required=True,type=Path)
    ap.add_argument('--scratch',required=True,type=Path)
    args=ap.parse_args()
    root=Path(__file__).resolve().parents[1]
    args.scratch.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='capability-native-',dir=args.scratch) as tmp:
        lab=Path(tmp);home=lab/'home';home.mkdir();hroot=home/'.hermes';hroot.mkdir()
        os.environ['HOME']=str(home);os.environ['HERMES_HOME']=str(hroot)
        os.environ['TMPDIR']=str(lab)
        os.environ.pop('HERMES_PROFILE',None)
        sys.path.insert(0,str(args.hermes_source.resolve()))
        from hermes_constants import get_default_hermes_root
        from hermes_cli.profile_distribution import install_distribution,update_distribution,DistributionError
        from hermes_cli.profiles import get_profile_dir
        from hermes_cli.plugin_packs import parse_pack
        from tools.skills_tool import skills_list,clear_skills_cache
        from tools.skills_sync import sync_skills
        assert get_default_hermes_root().resolve()==hroot.resolve()
        rows=json.loads((root/'capabilities/profiles.json').read_text())['profiles']
        installed=discovered=packs=updated=collisions=0
        def no_network(*_a,**_kw):raise AssertionError('network forbidden in native packaging proof')
        with patch.object(socket.socket,'connect',no_network),patch.object(socket,'create_connection',no_network):
            for row in rows:
                os.environ['HERMES_HOME']=str(hroot)
                plan=install_distribution(str(root/row['path']),create_alias=False)
                target=plan.target_dir.resolve();assert target.is_relative_to(lab)
                assert target==get_profile_dir(row['profile']).resolve()
                assert (target/'SOUL.md').read_bytes()==(root/row['path']/'SOUL.md').read_bytes()
                # Verify every source skill/reference/script/template, not just SKILL.md.
                for source in (root/row['path']/'skills').rglob('*'):
                    if source.is_file() and '__pycache__' not in source.parts:
                        assert (target/'skills'/source.relative_to(root/row['path']/'skills')).read_bytes()==source.read_bytes()
                os.environ['HERMES_HOME']=str(target)
                sync_skills(quiet=True)
                sync_skills(quiet=True)  # repeated startup must not replace reviewed shipped content
                for source in (root/row['path']/'skills').rglob('*'):
                    if source.is_file() and '__pycache__' not in source.parts:
                        assert (target/'skills'/source.relative_to(root/row['path']/'skills')).read_bytes()==source.read_bytes()
                clear_skills_cache()
                value=json.loads(skills_list())
                names={s['name'] for s in value.get('skills',[])}
                expected=set(row['existing_skills'])|{s['name'] for s in row['skills']}|{'profile-capabilities'}
                assert expected<=names,(row['profile'],sorted(expected-names),value.keys())
                assert len(names)==len(value.get('skills',[])),row['profile']
                cfg=target/'config.yaml'
                if row.get('config_seed'):
                    settings=json.loads(cfg.read_text());assert all(s['enabled'] is False for s in settings['mcp_servers'].values())
                guide=target/'skills/capabilities/profile-capabilities/references'
                pack=guide/'hermes-pack.yaml'
                if pack.exists():parse_pack(pack.read_text());packs+=1
                installed+=1;discovered+=len(expected)
            for name in ['agency-backend-engineer','council-travel-planner','academy-chemistry-professor','hermes-wear']:
                os.environ['HERMES_HOME']=str(hroot);target=get_profile_dir(name)
                # User-owned separate roots survive updates. Same-name shipped roots are replaced.
                own=target/'skills/capabilities/user-owned-skill/SKILL.md';own.parent.mkdir();own.write_text('user-owned fixture')
                note=target/'memories/native-proof.txt';note.write_text('synthetic user-owned note')
                cfg=target/'config.yaml';cfg.write_text('display:\n  skin: user-choice\n')
                shipped=target/'skills/capabilities/profile-capabilities/SKILL.md';shipped.write_text('edited shipped fixture')
                update_distribution(name)
                assert own.read_text()=='user-owned fixture' and note.read_text()=='synthetic user-owned note'
                assert cfg.read_text()=='display:\n  skin: user-choice\n'
                assert 'edited shipped fixture' not in shipped.read_text()
                updated+=1
                # Existing-profile install refuses without --force (no clobber).
                try:install_distribution(str(root/next(r['path'] for r in rows if r['profile']==name)))
                except DistributionError:collisions+=1
                else:raise AssertionError('existing install did not fail closed')
        print(json.dumps({'status':'PASS','installed_profiles':installed,'discovered_expected_skills':discovered,'native_plugin_packs_parsed':packs,'update_preservation_cases':updated,'existing_install_refusals':collisions,'network':'blocked during all install/discovery/update operations','limitations':'No account authentication, plugin activation, MCP tool calls, or model-based behavioral certification.'},indent=2))

if __name__=='__main__':main()
