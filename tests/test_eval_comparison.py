"""Synthetic comparison contracts, not live profile evaluations."""
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

from evals.core import ROOT, compare_runs, digest, grade, load_cases, profile_files, review_template
from evals.run import run_command


class ComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case = next(c for c in load_cases() if c['id'] == 'S03')

    def run_fixture(self, status='PASS', reviewed=True):
        case = self.case
        record = dict(mode='native', execution_status='COMPLETE', finals=['Synthetic answer'], events=[],
                      case_id=case['id'], profile=case['profile'], case_hash=case['case_hash'], repetition=0,
                      evidence_hash='fixture', usage=dict(complete=True, input_tokens=100, output_tokens=20, cached_input_tokens=0))
        review = review_template(case, record)
        review.update(reviewer='Synthetic reviewer', rationale='Test fixture only', evidence_ids=['final:0'],
                      requirements=[status != 'FAIL'] * len(case['expected']), prohibited_observed=[False] * len(case['prohibited']),
                      quality={q: 2 for q in case['quality_criteria']}, success_claims_reviewed=True)
        record['grade'] = grade(case, record, review if reviewed else None)
        manifest = {k: 'fixed' for k in ['model', 'provider', 'base_url', 'runtime_commit', 'settings_hash', 'adapter_version', 'grader_version']}
        return dict(manifest=manifest, results=[record])

    def test_setup_baseline_and_live_pass_are_not_behavioral_comparison(self):
        base, candidate = self.run_fixture(), self.run_fixture()
        base['results'][0]['execution_status'] = 'PREFLIGHT'
        self.assertEqual(compare_runs(base, candidate)['status'], 'INCOMPATIBLE')
        base['results'][0]['execution_status'] = 'COMPLETE'
        base['manifest']['preflight'] = True
        self.assertEqual(compare_runs(base, candidate)['status'], 'INCOMPATIBLE')

    def test_empty_runs_are_rejected(self):
        base, candidate = self.run_fixture(), self.run_fixture()
        for b, c in [([], []), (base['results'], []), ([], candidate['results'])]:
            self.assertEqual(compare_runs(dict(base, results=b), dict(candidate, results=c))['status'], 'INCOMPATIBLE')

    def test_unreviewed_baseline_and_reviewed_pass_lack_evidence(self):
        base, candidate = self.run_fixture(reviewed=False), self.run_fixture()
        for b, c in [(base, candidate), (candidate, base)]:
            result = compare_runs(b, c)
            self.assertEqual(result['status'], 'INCOMPLETE')
            self.assertEqual(result['changes'][0]['transition'], 'incomplete')
            self.assertIsNone(result['changes'][0]['token_ratio'])
        # A deterministic FAIL can still lack semantic review.
        base['results'][0]['grade']['status'] = 'FAIL'
        self.assertEqual(compare_runs(base, candidate)['changes'][0]['transition'], 'incomplete')

    def test_reviewed_fail_to_pass_and_pass_to_fail(self):
        failed, passed = self.run_fixture('FAIL'), self.run_fixture()
        result = compare_runs(failed, passed)
        self.assertEqual(result['changes'][0]['transition'], 'improved')
        self.assertIn('this trial', result['changes'][0]['observation'])
        self.assertEqual(compare_runs(passed, failed)['status'], 'REGRESSION')
        for run in [failed, passed]:
            self.assertEqual(compare_runs(run, run)['changes'][0]['transition'], 'unchanged')

    def test_regressions_and_incomplete_pairs_are_both_reported(self):
        base, candidate = self.run_fixture(), self.run_fixture('FAIL')
        for run in [base, candidate]:
            second = copy.deepcopy(run['results'][0]); second['repetition'] = 1
            run['results'].append(second)
        base['results'][1]['grade']['status'] = 'NOT RUN'
        candidate['results'].reverse()  # Match by ID + repetition, not list position.
        result = compare_runs(base, candidate)
        self.assertEqual(result['status'], 'REGRESSION_AND_INCOMPLETE')
        self.assertEqual(result['counts'], dict(regressed=1, incomplete=1, improved=0, unchanged=0))
        self.assertTrue(result['has_regressions'] and result['has_incomplete'])

    def test_compatibility_guards_and_duplicate_trials(self):
        base = self.run_fixture()
        for key in ['model', 'provider', 'base_url', 'runtime_commit', 'settings_hash', 'adapter_version', 'grader_version', 'browser_version']:
            candidate = copy.deepcopy(base); candidate['manifest'][key] = 'changed'
            self.assertEqual(compare_runs(base, candidate)['status'], 'INCOMPATIBLE', key)
        candidate = copy.deepcopy(base); candidate['results'][0]['case_hash'] = 'changed'
        self.assertEqual(compare_runs(base, candidate)['status'], 'INCOMPATIBLE')
        candidate = copy.deepcopy(base); candidate['results'][0]['repetition'] = 1
        self.assertEqual(compare_runs(base, candidate)['status'], 'INCOMPATIBLE')
        candidate = copy.deepcopy(base); candidate['results'] *= 2
        with self.assertRaises(ValueError): compare_runs(base, candidate)

    def test_token_comparison_requires_reviewed_passes_usage_and_cache_match(self):
        base, candidate = self.run_fixture(), self.run_fixture()
        candidate['results'][0]['usage']['input_tokens'] = 40
        self.assertEqual(compare_runs(base, candidate)['changes'][0]['token_ratio'], .5)
        for change in [dict(complete=False), dict(cached_input_tokens=10)]:
            other = copy.deepcopy(candidate); other['results'][0]['usage'].update(change)
            self.assertIsNone(compare_runs(base, other)['changes'][0]['token_ratio'])
        base['results'][0]['usage'].update(input_tokens=0, output_tokens=0)
        self.assertIsNone(compare_runs(base, candidate)['changes'][0]['token_ratio'])

    def attach_files(self, run, files):
        record = run['results'][0]; record['profile_hash'] = digest(files)
        run['manifest']['profile_packages'] = {record['profile_hash']: dict(profile=record['profile'], files=files)}

    def test_file_changes_and_missing_legacy_provenance(self):
        base, candidate = self.run_fixture(), self.run_fixture()
        self.assertFalse(compare_runs(base, candidate)['changes'][0]['profile_changes']['available'])
        self.attach_files(base, {'SOUL.md': 'a'*64, 'old.md': 'b'*64, 'config.yaml': 'c'*64})
        self.attach_files(candidate, {'SOUL.md': 'd'*64, 'skills/check/SKILL.md': 'e'*64, 'config.yaml': 'c'*64})
        diff = compare_runs(base, candidate)['changes'][0]['profile_changes']
        self.assertEqual([(f['path'], f['change']) for f in diff['files']], [('SOUL.md', 'changed'), ('old.md', 'removed'), ('skills/check/SKILL.md', 'added')])
        self.assertEqual(diff['unchanged_count'], 1)
        for path in ['/private/file', '../secret', 'C:\\private', 'a/../b']:
            self.attach_files(candidate, {path: 'a'*64})
            self.assertIsNone(profile_files(candidate, candidate['results'][0]))

    def test_legacy_reviewed_grades_remain_comparable(self):
        base, candidate = self.run_fixture(), self.run_fixture('FAIL')
        for run in [base, candidate]: del run['results'][0]['grade']['review_complete']
        self.assertEqual(compare_runs(base, candidate)['status'], 'REGRESSION')
        base['results'][0]['grade']['checks'] = []
        self.assertEqual(compare_runs(base, candidate)['status'], 'INCOMPLETE')

    def test_runner_uses_worker_source_manifest_not_later_checkout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'repo'; source = root / 'hermes-academy/profiles' / self.case['profile']
            source.mkdir(parents=True); (source / 'SOUL.md').write_text('before')
            output = Path(tmp) / 'results'
            files = {'SOUL.md': 'a'*64}
            def execute(*args):
                (source / 'SOUL.md').write_text('changed while worker ran')
                return dict(mode='native', execution_status='COMPLETE', events=[], finals=['Synthetic'], profile_files=files)
            args = SimpleNamespace(root=root, output=output, suite='pilot', case=None, model='test', provider='test', base_url='https://example.invalid',
                                   hermes_source=str(root), preflight=False, max_output_tokens=50, max_total_tokens=1000, limit=1, repeat=1, python='unused')
            with patch('evals.run.load_cases', return_value=[self.case]), patch('evals.run.execute', side_effect=execute), patch('evals.run.git_revision', return_value='fixed'):
                run_command(args)
            run = json.loads((output / 'results.json').read_text())
            self.assertEqual(profile_files(run, run['results'][0]), files)
            self.assertNotIn(str(root), json.dumps(run['manifest']))
            self.assertNotIn('changed while worker ran', json.dumps(run['manifest']))

    def test_source_snapshot_does_not_follow_later_edits(self):
        from evals.native_worker import snapshot_profile
        with tempfile.TemporaryDirectory() as tmp:
            source, target = Path(tmp) / 'source', Path(tmp) / 'snapshot'
            source.mkdir(); (source / 'SOUL.md').write_text('original')
            files = snapshot_profile(source, target)
            (source / 'SOUL.md').write_text('edited')
            self.assertEqual((target / 'SOUL.md').read_text(), 'original')
            from evals.core import tree_hashes
            self.assertEqual(tree_hashes(target), files)
            self.assertNotEqual(tree_hashes(source), files)

    def test_synthetic_examples_cannot_certify_live_behavior(self):
        base, candidate = self.run_fixture(), self.run_fixture()
        base['manifest']['synthetic'] = True
        self.assertEqual(compare_runs(base, candidate)['status'], 'INCOMPATIBLE')
        record = candidate['results'][0]; record['mode'] = 'synthetic'
        self.assertEqual(compare_runs(candidate, candidate)['status'], 'INCOMPLETE')
