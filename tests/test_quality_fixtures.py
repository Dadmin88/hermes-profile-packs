"""Structural integrity for synthetic behavioral fixtures, not a behavior verdict."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
QUALITY=ROOT/'docs/quality'

class QualityFixtureTests(unittest.TestCase):
    def cases(self):
        return [case for path in sorted(QUALITY.glob('*cases.json'))
                for case in json.loads(path.read_text())['cases']]

    def test_case_inventory_and_referenced_source_are_complete(self):
        cases=self.cases()
        self.assertEqual(175,len(cases))
        self.assertEqual(175,len({case['id'] for case in cases}))
        self.assertEqual(51,len({case['profile'] for case in cases}))
        self.assertEqual(179,sum(len(case['messages']) for case in cases))
        for case in cases:
            pack='academy' if case['profile'].startswith('academy-') else 'council'
            profile=ROOT/f'hermes-{pack}/profiles'/case['profile']
            self.assertTrue((profile/'SOUL.md').is_file(),case['id'])
            self.assertEqual('not_run',case['status'])
            for message in case['messages']:
                self.assertEqual('user',message['role'])
                self.assertTrue(message['content'].strip())
            for skill in case.get('skills',[]):
                target=ROOT/skill if '/' in skill else profile/'skills'/skill/'SKILL.md'
                self.assertTrue(target.is_file(),(case['id'],skill))

    def test_focused_humanities_checks_supply_the_work_to_review(self):
        required={
            'academy-law-professor-already-understands':('fictional classroom jurisdiction','Supplied rule:','My distinction:'),
            'academy-social-sciences-professor-already-understands':('My construct is','My proposed measure'),
            'academy-economics-professor-already-understands':('My assumption is','holding income'),
            'academy-business-professor-already-understands':('My interpretation is:','made on credit'),
            'academy-research-methods-professor-already-understands':('My construct is','My proposed measure'),
            'academy-arts-design-instructor-already-understands':('My distinction is','from this description'),
        }
        indexed={case['id']:case for case in self.cases()}
        for name,fragments in required.items():
            content=indexed[name]['messages'][0]['content']
            for fragment in fragments:self.assertIn(fragment,content,name)

    def test_evaluator_fixture_answers_are_not_learner_messages(self):
        cases=[case for case in self.cases() if case.get('evaluator_key')]
        self.assertEqual(15,len(cases))
        for case in cases:
            answer=case['evaluator_key']['reference_answer']
            for message in case['messages']:self.assertNotIn(answer,message['content'])
        # Instructor references intentionally contain keys. This checks prompt
        # separation only, never claims a blind mastery benchmark.

    def test_declined_memory_does_not_promise_zero_host_chat_history(self):
        case=next(case for case in self.cases() if case['id']=='H01')
        content=case['messages'][0]['content']
        self.assertIn('Do not add persistent memory',content)
        self.assertIn('ordinary chat history may still be recorded',content)
        self.assertTrue(case['observed_checks'])

if __name__=='__main__':unittest.main()
