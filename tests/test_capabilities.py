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
        self.assertEqual(167,len(names))

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

    def test_pixel_editors_ship_disabled_with_workflow_tools(self):
        profile = ROOT / 'hermes-agency/profiles/agency-pixel-artist'
        configs = json.loads((profile / 'config.yaml').read_text())['mcp_servers']
        self.assertEqual({'pixelorama', 'aseprite'}, set(configs))
        for config in configs.values():
            self.assertIs(False, config['enabled'])
            self.assertIs(False, config['supports_parallel_tool_calls'])
            self.assertIs(False, config['elicitation']['enabled'])
            self.assertIs(False, config['tools']['resources'])
            self.assertIs(False, config['tools']['prompts'])
        pixelorama = set(configs['pixelorama']['tools']['include'])
        self.assertTrue({'draw_pixels_fast', 'set_frame_duration', 'add_animation_tag',
                         'check_seamless_tile', 'export_animation'} <= pixelorama)
        self.assertNotIn('eval_gdscript', pixelorama)
        aseprite = set(configs['aseprite']['tools']['include'])
        self.assertTrue({'draw_grid', 'set_frame_duration', 'create_tag',
                         'create_tilemap_layer', 'export_spritesheet'} <= aseprite)

    def test_game_profiles_keep_distinct_tool_scopes(self):
        from capabilities import GUIDE, render_outputs
        data = json.loads((ROOT / 'capabilities/profiles.json').read_text())
        rows = {r['profile']: r for r in data['profiles'] if 'local_tools' in r}
        self.assertEqual(17, len(rows))
        selected = {}
        for name, row in rows.items():
            guide = ROOT / row['path'] / GUIDE
            catalog = json.loads((guide / 'references/catalog.json').read_text())
            self.assertEqual(row['local_tools'], [tool['name'] for tool in catalog['local_tools']])
            godot = next((m for m in catalog['mcps'] if m['name'] == 'godot'), None)
            if godot is None:
                continue
            cfg = godot['config']
            selected[name] = set(cfg['tools']['include'])
            self.assertIs(False, cfg['enabled'])
            self.assertFalse(selected[name].intersection(godot['required_tool_exclusions']))
            self.assertTrue((guide / godot['setup_patch']).is_file())
        self.assertEqual(14, len(selected))
        self.assertIn('set_cells', selected['agency-level-designer'])
        self.assertIn('send_key_sequence', selected['agency-qa-tester'])
        self.assertNotIn('set_cells', selected['agency-qa-tester'])
        self.assertIn('export_project', selected['agency-release-manager'])
        self.assertNotIn('export_project', selected['agency-art-director'])
        qa = next(m for m in rows['agency-qa-tester']['mcps'] if m['name'] == 'godot')
        qa['tools'].append('execute_script')
        with self.assertRaisesRegex(ValueError, 'invalid per-profile MCP tools'):
            render_outputs(ROOT, data)

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
