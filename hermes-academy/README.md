# Hermes Academy

Hermes Academy is the education profile pack for Hermes Agent: a faculty of professors and instructors that teaches academic subjects, technical disciplines, vocational skills, and professional foundations.

## The idea

Opening an Academy profile should feel like walking into the office, classroom, lab, studio, or training room of the instructor you need.

The initial faculty intentionally uses broad chairs that can later split into deeper departments. `academy-natural-sciences-professor` can eventually be joined by dedicated physics, chemistry, biology, astronomy, geology, and laboratory-methods faculty. `academy-skilled-trades-instructor` can later grow into welding, electrical, plumbing, carpentry, machining, automotive, HVAC, and other trade-specific instructors.

## Initial faculty

| Profile | Teaching domain |
| --- | --- |
| `academy-dean` | Faculty routing, learner brief, curriculum path, cross-faculty synthesis |
| `academy-mathematics-professor` | Mathematics and quantitative problem solving |
| `academy-writing-rhetoric-professor` | Writing, rhetoric, grammar, argument, revision |
| `academy-natural-sciences-professor` | Physics, chemistry, biology, scientific reasoning foundations |
| `academy-computer-science-professor` | Programming, algorithms, data structures, systems, computation |
| `academy-engineering-professor` | Engineering analysis, design, models, tradeoffs |
| `academy-history-professor` | Historical context, sources, causation, historiography |
| `academy-social-sciences-professor` | Psychology, sociology, political science, anthropology foundations |
| `academy-economics-professor` | Micro, macro, markets, models, policy reasoning |
| `academy-business-professor` | Accounting, finance, management, marketing, operations, strategy |
| `academy-language-instructor` | Language acquisition and conversation |
| `academy-research-methods-professor` | Research design, evidence, sources, methods, critique |
| `academy-skilled-trades-instructor` | Safety-first trade foundations, tools, measurement, procedures |
| `academy-health-sciences-professor` | Anatomy, physiology, terminology, health-science reasoning |
| `academy-arts-design-instructor` | Art/design fundamentals, critique, practice, portfolio learning |

## Teaching philosophy

Academy exists to help people **learn**, not merely receive plausible answers. Profiles adapt to learner level, explain concepts, demonstrate reasoning, provide guided practice, check understanding, correct misconceptions, and build transferable capability.

Professors and instructors may answer directly when that is what the learner wants. They should not manufacture friction or force a quiz. But when the goal is learning, they should teach in a way that makes the learner progressively less dependent on the profile.

Academy profiles do not claim to award grades, credentials, licenses, certifications, or professional authority. High-risk technical or health instruction remains educational and respects appropriate real-world supervision, codes, standards, and professional boundaries.

## Install

```bash
python install.py --list
python install.py academy-mathematics-professor academy-language-instructor
python install.py
```
