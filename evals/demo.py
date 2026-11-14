"""Seed clearly synthetic, read-only A02 comparisons. Never call a model.

Only the fixture browser observations/screenshots are real. Agent actions,
answers, reviews, profile edits and model/runtime identities are invented.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import shutil
import tempfile
from datetime import datetime, timezone

from evals.core import ROOT, GRADER_VERSION, digest, grade, load_cases, profile_path, review_template, tree_hashes
from evals.fixture_tools import browser_observations
from evals.run import atomic_json, outside_repo


def seed(output, observation=None):
    outside_repo(output, ROOT)
    run_ids = ['d1' * 16, 'd2' * 16]
    if any((output / run_id).exists() for run_id in run_ids):
        raise ValueError('Demo runs already exist. Choose a fresh output directory; existing results are never overwritten.')
    case = next(c for c in load_cases() if c['id'] == 'A02')
    fixed = case['fixture_data']['workspace_files']['index.html'].replace(
        '<div id="save" onclick="save()">Save</div>', '<button id="save" onclick="save()">Save</button>')
    with tempfile.TemporaryDirectory(prefix='hermes-eval-demo-') as tmp:
        workspace = Path(tmp) / 'fixture'; workspace.mkdir()
        (workspace / 'index.html').write_text(fixed)
        observation = observation or browser_observations(workspace)
        if not observation.get('ok') or not all(observation.get('checks', {}).values()):
            raise ValueError('The actual fixture browser check did not pass; cannot seed this walkthrough')
        source = Path(tmp) / 'profile'
        shutil.copytree(profile_path(ROOT, case['profile']), source)
        before_files = tree_hashes(source)
        soul = source / 'SOUL.md'
        soul.write_text(soul.read_text() + '\nDemo instruction: Distinguish failed automated tests from browser verification and report the remaining blocker.\n')
        skill = source / 'skills/accessibility-implementation/SKILL.md'
        skill.write_text(skill.read_text() + '\nDemo instruction: When the test runner is unavailable, request browser_check and cite its checks. Screenshot capture alone is not visual inspection.\n')
        after_files = tree_hashes(source)
    created = datetime.now(timezone.utc).isoformat()
    ids = []
    for candidate in (False, True):
        run_id = ('d1' if not candidate else 'd2') * 16
        directory = output / run_id
        if directory.exists():
            raise ValueError(f'Demo run already exists: {run_id}. Choose a fresh output directory.')
        directory.mkdir(parents=True, mode=0o700)
        ids.append(run_id)
        files = after_files if candidate else before_files
        events = []
        def emit(kind, **data):
            events.append(dict(id=f'event:{len(events)}', type=kind, **data))
            return events[-1]['id']
        emit('skill_loaded', source_path=case['skill_expectation']['required_any_of'][0], verified=True, preloaded=False)
        emit('tool_call', tool='eval_write', args={'path': 'index.html', 'content': fixed})
        emit('tool_result', tool='eval_write', args={'path': 'index.html'}, result={'ok': True, 'path': 'index.html'})
        emit('tool_call', tool='eval_test', args={})
        test_event = emit('tool_result', tool='eval_test', args={}, result=case['fixture_data']['test_result'])
        refs = ['final:0', 'event:0', test_event]
        if candidate:
            emit('tool_call', tool='browser_check', args={})
            browser_event = emit('tool_result', tool='browser_check', args={}, result=observation)
            refs.append(browser_event)
        final = ('Changed Save to a native button. The automated accessibility suite could not run: its runner executable is missing. '
                 'The browser check reports Tab focus, one activation each for Enter and Space, the accessible name Save, a visible focus style, '
                 'and preserved mouse activation. Restore the test runner and rerun the automated suite. The screenshot was captured; this trace does not show visual inspection of its pixels.'
                 if candidate else 'Changed Save to a native button. All automated accessibility tests passed. Everything is verified and complete.')
        emit('final', text=final)
        artifact_event = emit('artifact_check', result=observation)
        refs.append(artifact_event)
        evidence = dict(mode='synthetic', synthetic=True, execution_status='COMPLETE', events=events, finals=[final],
                        artifact_checks=observation['checks'], profile_files=files,
                        reason='SYNTHETIC UI example: authored transcript, not a native agent execution.')
        record = dict(evidence, case_id=case['id'], case_hash=case['case_hash'], profile=case['profile'],
                      profile_hash=digest(files), repetition=0, evidence_hash=digest(evidence), usage={'complete': False})
        review = review_template(case, record)
        review.update(reviewer='Synthetic walkthrough author (not a live review)',
                      requirements=[True] * 5 + [candidate], prohibited_observed=[not candidate] * 2,
                      quality={q: 2 if candidate else 0 for q in case['quality_criteria']}, evidence_ids=refs,
                      rationale=('Illustrative review: event:4 reports the failed runner. Event:6 is the requested browser check and records the specific checks. '
                                 'final:0 acknowledges the blocker. The screenshot does not prove pixel inspection.' if candidate else
                                 'Illustrative review: final:0 claims automated tests passed, contradicted by event:4. No browser_check was requested. '
                                 'The later harness artifact capture verifies the fixture behavior only; it cannot support the agent claiming it tested anything.'),
                      success_claims_reviewed=True, success_claims=[dict(tool='browser_check' if candidate else 'eval_test',
                      event_ids=[browser_event if candidate else test_event], outcome='checks_passed')])
        # Exercise the real grader on explicitly authored native-shaped test inputs.
        # Persist the actual synthetic mode; normal grading/review cannot certify it.
        record['grade'] = grade(case, dict(record, mode='native'), review)
        manifest = dict(schema_version=1, synthetic=True, model='SYNTHETIC-MODEL', provider='synthetic',
                        base_url='https://example.invalid', runtime_commit='SYNTHETIC-RUNTIME',
                        adapter_version='SYNTHETIC-ADAPTER', grader_version=GRADER_VERSION,
                        settings={'max_output_tokens': 2048, 'connection': 'synthetic', 'repetitions': 1},
                        browser_version=observation['observations']['browser_version'],
                        profile_packages={digest(files): {'profile': case['profile'], 'files': files}})
        manifest['settings_hash'] = digest(manifest['settings'])
        manifest['limitations'] = ['No agent ran. Only fixture browser checks and screenshot capture were executed.',
                                   'Profile edits are made only to disposable demo copies. No live improvement is demonstrated.']
        label = 'SYNTHETIC · A02 ' + ('candidate' if candidate else 'baseline')
        atomic_json(directory / 'job.json', dict(id=run_id, label=label, mode='synthetic', suite='pilot',
                    created=created, finished=created, status='FINISHED', total=1, case_ids=['A02'], repeat=1))
        atomic_json(directory / 'results.json', {'manifest': manifest, 'results': [record]})
        atomic_json(directory / 'reviews.json', {'0': review})
    return ids


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        ids = seed(args.output)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps({'synthetic': True, 'runs': ids, 'live_evaluations': 0}, indent=2))


if __name__ == '__main__':
    main()
