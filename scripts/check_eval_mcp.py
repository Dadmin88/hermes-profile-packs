"""Operator smoke check using a real stdio MCP client. Never makes a model call."""
import argparse
import asyncio
import base64
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from evals.mcp_server import WorkbenchAPI


async def check(args):
    output = args.output.resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError('Keep acceptance evidence outside the repository')
    output.mkdir(parents=True, exist_ok=False)
    api = WorkbenchAPI(args.port)
    calls = []

    async def call(client, name, arguments):
        result = await client.call_tool(name, arguments)
        if result.isError:
            raise RuntimeError(result.structuredContent)
        calls.append(dict(tool=name, arguments=arguments, result=result.structuredContent))
        for block in result.content:
            if block.type == 'image':
                (output/'candidate-event-6.png').write_bytes(base64.b64decode(block.data))
        return result.structuredContent

    params = StdioServerParameters(command=sys.executable,
        args=['-m', 'evals.mcp_server', '--port', str(args.port), '--assistant-name', 'MCP acceptance client'],
        cwd=str(ROOT), env={'PYTHONPATH': str(ROOT)})
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as client:
            await client.initialize()
            names = [t.name for t in (await client.list_tools()).tools]
            assert 'eval_submit_review' not in names
            await call(client, 'eval_inspect_case', {'case_id': 'A02'})
            jobs = []
            offset = 0
            while True:
                page = await call(client, 'eval_list_runs', {'offset':offset, 'limit':100})
                jobs.extend(page['runs'])
                offset += len(page['runs'])
                if offset >= page['total']: break
            baseline = next(j['id'] for j in jobs if j['label'] == 'SYNTHETIC · A02 baseline')
            candidate = next(j['id'] for j in jobs if j['label'] == 'SYNTHETIC · A02 candidate')
            pair = dict(baseline=baseline, candidate=candidate)
            comparison = await call(client, 'eval_compare_runs', pair)
            browser_comparison = api.request('compare', pair)
            assert all(comparison[k] == v for k, v in browser_comparison.items())
            before = await call(client, 'eval_get_evidence', dict(run_id=baseline, case_id='A02', event_id='event:4'))
            after = await call(client, 'eval_get_evidence', dict(run_id=candidate, case_id='A02', event_id='event:6'))
            assert not before['event']['result']['ok']
            assert after['event']['result']['ok']
            assert (output/'candidate-event-6.png').is_file()
            for run_id, evidence in [(baseline, before), (candidate, after)]:
                detail = api.request('runs/' + run_id)
                record = next(r for r in detail['run']['results'] if (r['case_id'], r['repetition']) == ('A02', 0))
                event = next(e for e in record['events'] if e['id'] == evidence['event']['id'])
                assert event['result']['ok'] == evidence['event']['result']['ok']
            setup = None
            if args.start_setup:
                setup = await call(client, 'eval_start_setup_check', {'case_ids':['C01'], 'label':'MCP acceptance · C01 setup'})
                # Persist the ID immediately. An interrupted client must check history, not restart.
                (output/'started-run.json').write_text(json.dumps(setup, indent=2)+'\n')
                for _ in range(60):
                    status = await call(client, 'eval_run_status', {'run_id':setup['id']})
                    if status['status'] != 'RUNNING': break
                    await asyncio.sleep(1)
                assert status['status'] == 'FINISHED', 'Check existing run history; do not restart automatically'
                assert status['trials'][0]['kind'] == 'setup'
                assert not status['trials'][0]['behavioral_evidence_complete']
                assert any(j['id'] == setup['id'] for j in api.request('runs'))
                trial = await call(client, 'eval_inspect_trial', {'run_id':setup['id'], 'case_id':'C01'})
                # A compact copy of this installation-only run permits browser rendering checks.
                detail = api.request('runs/' + setup['id'])
                (output/'setup-browser-record.json').write_text(json.dumps({k:detail[k] for k in ['job','run','reviews']}, indent=2)+'\n')
                setup = dict(setup, final_status=status['status'], execution_status=trial['execution_status'])
    summary = dict(tools=len(names), comparison_matches_browser_api=True, evidence_matches_browser_api=True,
                   synthetic_pair=pair, screenshot='candidate-event-6.png', setup=setup, live_model_calls=0)
    (output/'calls.json').write_text(json.dumps(calls, indent=2)+'\n')
    (output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--output', type=Path, required=True, help='New directory outside the repository')
    parser.add_argument('--start-setup', action='store_true', help='Start exactly one C01 setup job (no model call)')
    asyncio.run(check(parser.parse_args()))
