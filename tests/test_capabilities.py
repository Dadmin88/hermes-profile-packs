"""Capability materialization must be exact, complete, offline and opt-in."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]

class CapabilityTests(unittest.TestCase):
    def test_materialized_catalog_is_complete_and_current(self):
        result=subprocess.run([sys.executable,str(ROOT/'capabilities.py'),'--check'],capture_output=True,text=True)
        self.assertEqual(0,result.returncode,result.stdout+result.stderr)

    def test_all_source_distributions_have_exactly_one_record(self):
        records=json.loads((ROOT/'capabilities/profiles.json').read_text())['profiles']
        names=[r['profile'] for r in records]
        actual={p.parent.relative_to(ROOT).as_posix() for p in ROOT.glob('hermes-*/profiles/*/distribution.yaml')}
        actual.add('hermes-wear')
        self.assertEqual(len(names),len(set(names)))
        self.assertEqual(actual,{r['path'] for r in records})
        self.assertEqual(166,len(names))

    def test_native_jobs_remain_role_owned(self):
        for pack in ['academy','council']:
            manifest=json.loads((ROOT/f'hermes-{pack}/{pack}.json').read_text())
            for r in manifest['profiles']:
                skills={p.parent.name for p in (ROOT/f'hermes-{pack}/profiles'/r['name']/'skills').glob('*/SKILL.md')}
                if pack=='academy':skills.discard('teach-profile')
                self.assertEqual(set(r['jobs']),skills)

    def test_integrations_never_auto_activate(self):
        data=json.loads((ROOT/'capabilities/profiles.json').read_text())
        for r in data['profiles']:
            guide=ROOT/r['path']/'skills/capabilities/profile-capabilities/references/catalog.json'
            self.assertTrue(guide.is_file(),r['profile'])
            cfg=json.loads(guide.read_text())
            for m in cfg['mcps']:
                self.assertIs(False,m['config']['enabled'])
                self.assertIs(False,m['config']['sampling']['enabled'])
            for p in cfg['plugins']:
                self.assertIn('--no-enable',p['install_command'])
                self.assertIn('--no-deps',p['install_command'])

    def test_narrow_profiles_are_not_given_execution_bundles(self):
        rows=json.loads((ROOT/'capabilities/profiles.json').read_text())['profiles']
        for r in rows:
            if r['profile'] in {'hermes-wear','agency-orchestrator','academy-dean','council-steward'}:
                self.assertEqual([],r['skills'])
                self.assertEqual([],r['plugins'])
                self.assertEqual([],r['mcps'])

    def test_seed_shadows_are_identical_and_not_extra_capabilities(self):
        rows=json.loads((ROOT/'capabilities/profiles.json').read_text())['profiles']
        for row in rows:
            for shadow in row.get('seed_shadows',[]):
                source=ROOT/row['path']/shadow['source']
                target=ROOT/row['path']/shadow['destination']
                files={str(p.relative_to(source)):p.read_bytes() for p in source.rglob('*') if p.is_file()}
                copied={str(p.relative_to(target)):p.read_bytes() for p in target.rglob('*') if p.is_file()}
                self.assertEqual(files,copied)
                self.assertIn(shadow['name'],row['existing_skills'])

    def test_selected_bundles_use_native_paths(self):
        lock=json.loads((ROOT/'capabilities/skills.lock.json').read_text())['skills']
        for name,row in lock.items():
            if row['repository']=='https://github.com/NousResearch/hermes-agent' and row['path'].startswith('skills/'):
                self.assertEqual(row['path'],row['install_path'])

    def test_selection_error_is_fail_closed(self):
        import capabilities
        data=capabilities.load_json(ROOT/'capabilities/profiles.json')
        data['profiles'][0]['skills'].append({'name':'not-a-reviewed-skill','reason':'test'})
        with self.assertRaises(ValueError):capabilities.render_outputs(ROOT,data)

if __name__=='__main__':unittest.main()
