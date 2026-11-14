"""Workbench orchestration/security tests; synthetic records are not behavioral passes."""
import copy
from io import BytesIO
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from evals.core import ROOT, digest, grade, review_template
from evals.run import atomic_json
from evals.workbench import Workbench, handler_for


class WorkbenchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.app = Workbench(ROOT, Path(self.temp.name) / 'runs', ROOT / 'not-a-runtime')

    def fixture(self, execution='COMPLETE'):
        case = self.app.cases['S03']
        evidence = {'mode': 'native', 'execution_status': execution, 'events': [], 'finals': ['Synthetic queue explanation'], 'artifact_checks': {}}
        record = {**evidence, 'case_id': case['id'], 'case_hash': case['case_hash'], 'profile': case['profile'],
                  'profile_hash': 'fixture', 'repetition': 0, 'evidence_hash': digest(evidence), 'usage': {'complete': False}}
        record['grade'] = grade(case, record)
        run_id = 'a' * 32
        path = self.app.output / run_id
        path.mkdir()
        atomic_json(path / 'job.json', {'id': run_id, 'created': '2026-01-01', 'status': 'FINISHED', 'total': 1})
        atomic_json(path / 'results.json', {'manifest': {}, 'results': [record]})
        review = review_template(case, record)
        review.update(reviewer='test-only', rationale='Synthetic review', requirements=[True]*len(case['expected']),
                      prohibited_observed=[False]*len(case['prohibited']), quality={q:2 for q in case['quality_criteria']},
                      evidence_ids=['final:0'], success_claims_reviewed=True)
        return run_id, path, review

    def test_catalog_matches_pilot_and_canonical_suites(self):
        self.assertEqual([len(self.app.catalogs[k]) for k in ('pilot', 'existing', 'all')], [18, 175, 190])

    def test_secret_never_in_bootstrap(self):
        with patch.dict(os.environ, {'HERMES_EVAL_API_KEY': 'synthetic-secret'}):
            result = self.app.bootstrap()
        self.assertTrue(result['credential_configured'])
        self.assertNotIn('synthetic-secret', json.dumps(result))

    def test_budgets_and_case_ids_fail_before_spawning(self):
        for data in ({'case_ids': ['C01'], 'repeat': -1}, {'case_ids': ['C01'], 'max_total_tokens': 1000001},
                     {'case_ids': ['C01'], 'repeat': True}, {'case_ids': ['does-not-exist']},
                     {'case_ids': ['C01', 'C01']}, {'case_ids': ['C01'], 'mode': 'unknown'}):
            with self.subTest(data=data), patch('evals.workbench.subprocess.Popen') as spawn:
                with self.assertRaises(ValueError): self.app.start(data)
                spawn.assert_not_called()

    def test_live_requires_explicit_credentials(self):
        with patch.dict(os.environ, {}, clear=True), patch('evals.workbench.subprocess.Popen') as spawn:
            with self.assertRaisesRegex(ValueError, 'HERMES_EVAL_API_KEY'):
                self.app.start({'case_ids':['C01'], 'mode':'live', 'model':'test', 'provider':'openai', 'base_url':'https://example.invalid/v1'})
            spawn.assert_not_called()

    def test_shell_text_is_passed_as_literal_argument(self):
        with patch('evals.workbench.subprocess.Popen') as spawn, patch('evals.workbench.threading.Thread'):
            spawn.return_value.poll.return_value = None
            self.app.start({'case_ids':['C01'], 'model':'$(touch /tmp/should-never-exist)'})
            args, kwargs = spawn.call_args
            self.assertIn('$(touch /tmp/should-never-exist)', args[0])
            self.assertNotIn('shell', kwargs)
            with self.assertRaisesRegex(ValueError, 'already active'): self.app.start({'case_ids':['C01']})
            self.app.cancel(self.app.active)
            spawn.return_value.terminate.assert_called_once()

    def test_review_persists_separately_and_reuses_grader(self):
        run_id, path, review = self.fixture()
        original = (path / 'results.json').read_bytes()
        verdict = self.app.review(run_id, 0, review)
        self.assertEqual(verdict['status'], 'PASS')
        self.assertEqual((path / 'results.json').read_bytes(), original)
        self.assertEqual(self.app.run_data(run_id)['run']['results'][0]['grade']['status'], 'PASS')
        self.assertEqual(self.app.jobs()[0]['counts']['PASS'], 1)
        review['requirements'][0] = False
        self.assertEqual(self.app.review(run_id, 0, review)['status'], 'FAIL')

    def test_review_rejects_changed_evidence_and_stale_hashes(self):
        run_id, path, review = self.fixture()
        stale = copy.deepcopy(review); stale['evidence_hash'] = 'wrong'
        with self.assertRaisesRegex(ValueError, 'does not match'): self.app.review(run_id, 0, stale)
        run = json.loads((path / 'results.json').read_text()); run['results'][0]['finals'] = ['tampered']
        atomic_json(path / 'results.json', run)
        with self.assertRaisesRegex(ValueError, 'altered'): self.app.review(run_id, 0, review)

    def test_review_cannot_certify_preflight_or_incomplete_review(self):
        run_id, _, review = self.fixture('PREFLIGHT')
        self.assertEqual(self.app.review(run_id, 0, review)['status'], 'BLOCKED')
        review['requirements'][0] = None
        self.assertEqual(self.app.review(run_id, 0, review)['status'], 'BLOCKED')

    def test_unsupported_success_claim_fails(self):
        run_id, _, review = self.fixture()
        review['success_claims'] = [{'tool':'eval_test', 'event_ids':['event:missing'], 'outcome':'checks_passed'}]
        self.assertEqual(self.app.review(run_id, 0, review)['status'], 'FAIL')

    def test_invalid_paths_and_partial_comparisons_rejected(self):
        for path in ('../outside', '/etc/passwd', 'abc'):
            with self.assertRaises(ValueError): self.app.directory(path)
        run_id, path, _ = self.fixture()
        job = json.loads((path/'job.json').read_text()); job['status']='CANCELLED'; atomic_json(path/'job.json', job)
        with self.assertRaisesRegex(ValueError, 'partial'): self.app.compare(run_id, run_id)

    def request(self, method, path, headers=None, body=None):
        handler = object.__new__(handler_for(self.app))
        handler.path = path
        handler.server = SimpleNamespace(server_port=8765)
        handler.headers = {'Host':'localhost:8765', **(headers or {})}
        handler.rfile = BytesIO(json.dumps(body).encode() if body is not None else b'')
        if body is not None: handler.headers['Content-Length'] = str(len(handler.rfile.getvalue()))
        captured=[]
        handler.send=lambda *args: captured.append(args)
        getattr(handler, 'do_' + method)()
        return captured[0]

    def test_http_same_origin_csrf_and_no_arbitrary_file_read(self):
        self.assertEqual(self.request('GET', '/api/bootstrap', {'Host':'attacker.test:8765'})[0], 403)
        self.assertEqual(self.request('GET', '/api/bootstrap', {'Origin':'https://evil.invalid'})[0], 403)
        self.assertEqual(self.request('POST', '/api/runs', body={'case_ids':['C01']})[0], 403)
        self.assertEqual(self.request('GET', '/../../etc/passwd')[0], 404)
        self.assertEqual(self.request('GET', '/api/cases?suite=pilot')[0], 200)
        self.assertEqual(self.request('GET', '/')[2], 'text/html')
        headers={'Content-Type':'application/json','X-Workbench-Token':self.app.token}
        with patch.object(self.app, 'start', return_value={'status':'RUNNING'}) as start:
            self.assertEqual(self.request('POST', '/api/runs', headers, {'case_ids':['C01']})[0], 201)
            start.assert_called_once()

    def test_cancel_kills_isolated_native_worker(self):
        # Real process tree; no model, network, or Hermes imports needed.
        script = Path(self.temp.name) / 'wait-worker.py'
        pidfile = Path(self.temp.name) / 'worker.pid'
        script.write_text('import os,time\nfrom pathlib import Path\nPath(' + repr(str(pidfile)) + ').write_text(str(os.getpid()))\ntime.sleep(30)\n')
        controller = Path(self.temp.name) / 'controller.py'
        controller.write_text('from unittest.mock import patch\nimport subprocess,sys\nfrom evals.run import execute\noriginal=subprocess.Popen\ndef child(*args, **kwargs):\n return original([sys.executable,' + repr(str(script)) + '], **kwargs)\nwith patch("evals.run.subprocess.Popen", child):\n execute({},sys.executable,' + repr(str(ROOT)) + ',60)\n')
        env = dict(os.environ, PYTHONPATH=str(ROOT))
        process = subprocess.Popen([sys.executable, str(controller)], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.addCleanup(lambda: process.kill() if process.poll() is None else None)
        deadline = time.monotonic() + 5
        while not pidfile.exists() and time.monotonic() < deadline: time.sleep(.02)
        self.assertTrue(pidfile.exists())
        child = int(pidfile.read_text())
        process.terminate(); process.wait(timeout=5)
        with self.assertRaises(ProcessLookupError): os.kill(child, 0)


if __name__ == '__main__': unittest.main()
