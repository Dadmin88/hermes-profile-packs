"""Local API + real stdio protocol contracts; synthetic evidence, no model calls."""
import asyncio
import base64
from contextlib import asynccontextmanager
from io import BytesIO
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import ValidationError

from evals.core import ROOT, digest, grade, review_template
from evals.demo import seed
from evals.mcp_server import Adapter, AdapterError, Live, Setup, ReviewTrial, Run, Trial, WorkbenchAPI, build_server
from evals.run import atomic_json
from evals.workbench import ThreadingHTTPServer, Workbench, handler_for

# Test-only image bytes; the acceptance walkthrough uses an actual fixture capture.
PNG = base64.b64encode(b'\x89PNG\r\n\x1a\nsynthetic-test-image').decode()


class APIClientTests(unittest.TestCase):
    def response(self, value):
        response = Mock()
        response.__enter__ = Mock(return_value=BytesIO(json.dumps(value).encode()))
        response.__exit__ = Mock(return_value=False)
        return response

    def test_internal_token_is_used_and_refreshed_without_returning_it(self):
        api = WorkbenchAPI(4321)
        api.opener = Mock()
        api.opener.open.side_effect = [self.response({'csrf_token': 'first-secret'}), self.response({'id': 'a'*32}),
                                      self.response({'csrf_token': 'rotated-secret'}), self.response({'id': 'b'*32})]
        self.assertEqual(api.request('runs', {'mode': 'preflight'}, starting=True), {'id': 'a'*32})
        self.assertEqual(api.request('runs', {'mode': 'preflight'}, starting=True), {'id': 'b'*32})
        requests = [call.args[0] for call in api.opener.open.call_args_list]
        self.assertEqual(requests[1].get_header('X-workbench-token'), 'first-secret')
        self.assertEqual(requests[3].get_header('X-workbench-token'), 'rotated-secret')
        self.assertEqual(requests[1].get_header('Origin'), 'http://127.0.0.1:4321')
        self.assertFalse(any('secret' in r.full_url for r in requests))

    def test_uncertain_start_is_never_retried(self):
        for error in [TimeoutError(), URLError('connection reset'), ValueError('invalid JSON'),
                      HTTPError('local', 500, 'error', {}, BytesIO(b'{}'))]:
            api = WorkbenchAPI(); api.opener = Mock()
            api.opener.open.side_effect = [self.response({'csrf_token': 'private'}), error]
            with self.assertRaises(AdapterError) as caught:
                api.request('runs', {'mode': 'live'}, starting=True)
            self.assertEqual(caught.exception.code, 'START_OUTCOME_UNKNOWN')
            self.assertIn('history', caught.exception.message)
            self.assertEqual(api.opener.open.call_count, 2)

    def test_unreachable_bootstrap_does_not_claim_a_start_was_sent(self):
        api = WorkbenchAPI(); api.opener = Mock()
        api.opener.open.side_effect = URLError('refused')
        with self.assertRaises(AdapterError) as caught: api.request('runs', {}, starting=True)
        self.assertEqual(caught.exception.code, 'UNREACHABLE')
        self.assertEqual(api.opener.open.call_count, 1)

    def test_token_rejection_and_error_body_do_not_leak(self):
        for code in [403, 400, 302]:
            api = WorkbenchAPI(); api.opener = Mock()
            api.opener.open.side_effect = [self.response({'csrf_token': 'private-token'}),
                HTTPError('local', code, 'private-token', {}, BytesIO(b'{"error":"private-token"}'))]
            with self.assertRaises(AdapterError) as caught: api.request('runs', {})
            self.assertNotIn('private-token', str(caught.exception))
            self.assertEqual(api.opener.open.call_count, 2)

    def test_only_loopback_and_bounded_run_inputs(self):
        for port in [0, 65536, True, 'http://example.invalid']:
            with self.assertRaises(ValueError): WorkbenchAPI(port)
        for changes in [{'base_url':'http://evil.invalid'}, {'command':'sh'}, {'profile_source':'/tmp'},
                        {'max_total_tokens':0}, {'max_total_tokens':True}, {'max_total_tokens':1000001}, {'repeat':6}]:
            with self.assertRaises(ValidationError): Live.model_validate(dict(case_ids=['C01'], max_total_tokens=500) | changes)
        with self.assertRaises(ValidationError): Live.model_validate({'case_ids':['C01']})
        api = Mock(browser_origin='http://localhost:8765')
        api.request.return_value = {'id':'a'*32, 'mode':'live'}
        Adapter(api).start_live_run(Live(case_ids=['C01'], max_total_tokens=500))
        body = api.request.call_args.args[1]
        self.assertEqual(body['mode'], 'live')
        self.assertEqual(body['max_total_tokens'], 500)
        self.assertFalse({'model','provider','base_url','python','hermes_source'} & body.keys())
        from evals.mcp_server import NoRedirects
        self.assertIsNone(NoRedirects().redirect_request(None, None, None, None, None, None))


class MCPWorkflowTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.app = Workbench(ROOT, Path(self.temp.name)/'runs', ROOT/'not-a-runtime')
        observation = dict(ok=True, observations={'browser_version':'fixture-browser'}, screenshot_png_base64=PNG,
                           checks={name: True for name in self.app.cases['A02']['artifact_checks']})
        self.baseline, self.candidate = seed(self.app.output, observation)
        self.http = ThreadingHTTPServer(('127.0.0.1', 0), handler_for(self.app))
        self.port = self.http.server_port
        self.thread = threading.Thread(target=self.http.serve_forever, daemon=True); self.thread.start()
        self.addCleanup(self.http.server_close); self.addCleanup(self.http.shutdown)

    @asynccontextmanager
    async def client(self, submission=False, port=None):
        args = ['-m', 'evals.mcp_server', '--port', str(port or self.port), '--assistant-name', 'test assistant']
        if submission: args.append('--enable-review-submission')
        params = StdioServerParameters(command=sys.executable, args=args, cwd=str(ROOT), env={'PYTHONPATH':str(ROOT)})
        with tempfile.TemporaryFile(mode='w+') as errors:
            async with stdio_client(params, errlog=errors) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    yield session
            errors.seek(0)
            self.assertNotIn(self.app.token, errors.read())

    async def test_unavailable_server_through_actual_client(self):
        import socket
        # Reserve a loopback port without listening so no unrelated service is touched.
        with socket.socket() as unavailable:
            unavailable.bind(('127.0.0.1', 0))
            async with self.client(port=unavailable.getsockname()[1]) as client:
                for tool, args in [('eval_list_runs', {}), ('eval_start_setup_check', {'case_ids':['C01']})]:
                    result = await self.call(client, tool, args)
                    self.assertTrue(result.isError)
                    self.assertEqual(result.structuredContent['error']['code'], 'UNREACHABLE')

    async def call(self, client, name, args):
        result = await client.call_tool(name, args)
        self.assertNotIn(self.app.token, result.model_dump_json())
        return result

    async def test_actual_stdio_compare_evidence_and_images_match_http(self):
        async with self.client() as client:
            tools = (await client.list_tools()).tools
            self.assertNotIn('eval_submit_review', [t.name for t in tools])
            self.assertTrue(all(t.description and t.inputSchema.get('additionalProperties') is False for t in tools))
            listed = await self.call(client, 'eval_list_cases', {'suite':'pilot', 'profile':'agency-frontend-engineer'})
            self.assertEqual(listed.structuredContent['total'], 6)
            case = await self.call(client, 'eval_inspect_case', {'case_id':'A02'})
            self.assertIn('expected', case.structuredContent)
            compared = await self.call(client, 'eval_compare_runs', {'baseline':self.baseline,'candidate':self.candidate})
            self.assertFalse(compared.isError)
            self.assertEqual(compared.structuredContent['changes'], self.app.compare(self.baseline,self.candidate)['changes'])
            self.assertNotIn('screenshot_png_base64', compared.model_dump_json())
            self.assertNotIn(PNG, compared.model_dump_json())
            event = await self.call(client, 'eval_get_evidence', {'run_id':self.baseline,'case_id':'A02','event_id':'event:4'})
            self.assertFalse(event.structuredContent['event']['result']['ok'])
            image = await self.call(client, 'eval_get_evidence', {'run_id':self.candidate,'case_id':'A02','event_id':'event:6'})
            self.assertEqual([c.type for c in image.content], ['text','image'])
            self.assertEqual(image.content[1].data, PNG)
            self.assertEqual(image.structuredContent['capture_source'], 'Capture returned by browser_check')
            self.assertIn('does not establish', image.structuredContent['pixel_inspection'])
            artifact = await self.call(client, 'eval_get_evidence', {'run_id':self.baseline,'case_id':'A02','event_id':'event:6'})
            self.assertEqual(artifact.structuredContent['capture_source'], 'Harness capture after the agent finished')
            for tool, args in [('eval_list_runs', {}), ('eval_run_status', {'run_id':self.candidate}),
                               ('eval_inspect_trial', {'run_id':self.candidate,'case_id':'A02'})]:
                result = await self.call(client, tool, args)
                self.assertFalse(result.isError)
                self.assertNotIn(PNG, result.model_dump_json())
                self.assertNotIn('runner.log', result.model_dump_json())
            trial = await self.call(client, 'eval_inspect_trial', {'run_id':self.candidate,'case_id':'A02'})
            self.assertEqual(trial.structuredContent['kind'], 'synthetic')
            self.assertFalse(trial.structuredContent['behavioral_evidence_complete'])
            self.assertIn('#run=', trial.structuredContent['browser_url'])

    async def test_invalid_ids_overrides_busy_and_request_checks(self):
        async with self.client() as client:
            for tool, args in [('eval_run_status', {'run_id':'../outside'}),
                               ('eval_start_live_run', {'case_ids':['C01']}),
                               ('eval_start_setup_check', {'case_ids':['C01'],'base_url':'https://evil.invalid'}),
                               ('eval_get_evidence', {'run_id':self.baseline,'case_id':'A02','event_id':'event:999'}),
                               ('eval_inspect_trial', {'run_id':self.baseline,'case_id':'A02','repetition':1}),
                               ('eval_inspect_case', {'case_id':'unknown'}),
                               ('eval_submit_review', {})]:
                result = await self.call(client, tool, args)
                self.assertTrue(result.isError, (tool, result))
            self.app.active = 'a'*32
            try:
                result = await self.call(client, 'eval_start_setup_check', {'case_ids':['C01']})
                self.assertEqual(result.structuredContent['error']['code'], 'BUSY')
            finally: self.app.active = None
            # A rotated token is fetched internally for the next POST.
            self.app.token = 'rotated-private-token'
            result = await self.call(client, 'eval_compare_runs', {'baseline':self.baseline,'candidate':self.candidate})
            self.assertFalse(result.isError)

    async def test_setup_is_server_owned_and_visible_in_shared_history(self):
        async with self.client() as client:
            result = await self.call(client, 'eval_start_setup_check', {'case_ids':['C01'], 'label':'MCP contract setup'})
            self.assertFalse(result.isError)
            run_id = result.structuredContent['id']
            self.assertEqual(self.app.run_data(run_id)['job']['label'], 'MCP contract setup')
            # Missing native runtime will produce a genuine blocked setup result.
            for _ in range(100):
                result = await self.call(client, 'eval_run_status', {'run_id':run_id})
                if result.structuredContent['status'] != 'RUNNING': break
                await asyncio.sleep(.05)
            self.assertEqual(result.structuredContent['trials'][0]['kind'], 'setup')
            self.assertFalse(result.structuredContent['trials'][0]['behavioral_evidence_complete'])

    async def test_cancel_calls_the_server(self):
        run_id = 'f'*32
        directory = self.app.output/run_id; directory.mkdir()
        atomic_json(directory/'job.json', dict(id=run_id, status='RUNNING', created='test', total=1, mode='preflight'))
        self.app.active = run_id; self.app.process = Mock()
        self.app.process.poll.return_value = None
        try:
            async with self.client() as client:
                result = await self.call(client, 'eval_cancel_run', {'run_id':run_id})
                self.assertEqual(result.structuredContent['status'], 'CANCELLED')
                self.app.process.terminate.assert_called_once()
                self.assertEqual(self.app.run_data(run_id)['job']['status'], 'CANCELLED')
        finally: self.app.active = None; self.app.process = None

    async def test_review_proposal_is_unsaved_and_submission_is_gated(self):
        case = self.app.cases['S03']; run_id = 'a'*32
        directory = self.app.output/run_id; directory.mkdir()
        evidence = dict(mode='native', execution_status='COMPLETE', events=[], finals=['Synthetic unit test answer'])
        record = dict(evidence, case_id=case['id'], case_hash=case['case_hash'], profile=case['profile'], repetition=0,
                      evidence_hash=digest(evidence), usage={'complete':False})
        record['grade'] = grade(case, record)
        atomic_json(directory/'job.json', dict(id=run_id, status='FINISHED', mode='live', created='test', total=1))
        atomic_json(directory/'results.json', dict(manifest={}, results=[record]))
        review = review_template(case, record)
        review.update(requirements=[True]*len(case['expected']), prohibited_observed=[False]*len(case['prohibited']),
                      quality={q:2 for q in case['quality_criteria']}, evidence_ids=['final:0'], rationale='Synthetic unit test', success_claims_reviewed=True)
        del review['reviewer']; del review['case_id']
        args = dict(run_id=run_id, case_id='S03', review=review)
        async with self.client() as client:
            proposal = await self.call(client, 'eval_propose_review', args)
            self.assertFalse(proposal.isError)
            self.assertFalse(proposal.structuredContent['saved'])
            self.assertFalse((directory/'reviews.json').exists())
            self.assertEqual(proposal.structuredContent['reviewer'], 'Assistant: test assistant')
        async with self.client(submission=True) as client:
            self.assertIn('eval_submit_review', [t.name for t in (await client.list_tools()).tools])
            stale = json.loads(json.dumps(args)); stale['review']['evidence_hash']='stale'
            self.assertTrue((await self.call(client, 'eval_submit_review', stale)).isError)
            saved = await self.call(client, 'eval_submit_review', args)
            self.assertFalse(saved.isError)
            self.assertEqual(self.app.run_data(run_id)['reviews'][0]['reviewer'], 'Assistant: test assistant')
            self.assertEqual(self.app.run_data(run_id)['run']['results'][0]['grade']['status'], 'PASS')
