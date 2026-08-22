# Hermes Agency

Hermes Agency is a curated collection of **109 professional profiles for [Hermes Agent](https://github.com/NousResearch/hermes-agent)**.

The profiles form a multidisciplinary agency covering engineering, product, design, quality assurance, research, marketing, content, leadership, and operations. Each profile combines a focused professional role with bundled task skills, routing metadata, working standards, collaboration expectations, and clear handoff behavior.

Profiles can be used independently or coordinated through Hermes Kanban for multi-role work.

## Features

- **109 specialized profiles** spanning technical, creative, product, business, and operational work.
- **Bundled professional skills** that are installed with each profile and loaded by Hermes when relevant.
- **Hermes-native profile distributions** that install with standard Hermes profile tooling.
- **Routing-ready descriptions** so profiles can be selected by capability and responsibility.
- **Professional role definitions** with explicit responsibilities, operating standards, and definitions of done.
- **Shared collaboration rules** for cross-profile handoffs, independent review, evidence, and escalation.
- **Selective installation** so a machine can install the complete Agency or only the roles it needs.

## Requirements

- [Hermes Agent](https://github.com/NousResearch/hermes-agent)
- Python 3.10 or newer
- Git

## Installation

Clone the repository:

```bash
git clone https://github.com/Dadmin88/hermes-agency.git
cd hermes-agency
```

Install the complete Agency:

```bash
python3 install.py
```

Install selected profiles:

```bash
python3 install.py agency-orchestrator agency-backend-engineer agency-code-reviewer
```

List available profiles:

```bash
python3 install.py --list
```

Install a category:

```bash
python3 install.py --category engineering
```

Use `--force` to re-apply profiles that are already installed:

```bash
python3 install.py --force
```

The installer uses Hermes profile distributions and registers each profile's curated description with `hermes profile describe`.

## Quick start

The installer creates shell aliases for installed profiles. A profile can be used directly:

```bash
agency-market-researcher chat
agency-software-architect chat
agency-social-media-manager chat
```

For multi-role work, install `agency-orchestrator` together with the specialists you want available and use Hermes Kanban to assign work by profile name.

Example Hermes configuration:

```yaml
kanban:
  orchestrator_profile: agency-orchestrator
```

## Bundled skills

Every Agency profile ships with a `skills/` directory containing task-specific professional playbooks. Hermes profile distributions install those skills together with the profile, and Hermes can load them on demand when the profile encounters matching work.

The distinction is intentional:

- `SOUL.md` defines the specialist's role, authority, working standards, and collaboration behavior.
- `skills/` defines repeatable procedures for specific classes of work within that specialty.

For example, the Security Engineer includes a threat-modeling skill, the QA Tester includes an exploratory-testing skill, the Product Manager includes a product-requirements skill, and the Social Media Manager includes a social-content-plan skill.

Skill bundles are expected to grow as useful procedures are developed or curated. Third-party skills are reviewed and vendored into the profile rather than fetched from a public marketplace during profile installation.

## Profile roster

Hermes Agency currently includes:

| Area | Profiles |
|---|---:|
| Leadership & Coordination | 10 |
| Engineering | 26 |
| Quality & Review | 9 |
| Design & Creative | 18 |
| Product & Research | 14 |
| Marketing & Growth | 12 |
| Content & Editorial | 10 |
| Operations & Support | 10 |
| **Total** | **109** |

### Leadership & Coordination

| Profile | Role |
|---|---|
| `agency-business-continuity-manager` | Business Continuity Manager |
| `agency-chief-of-staff` | Chief of Staff |
| `agency-operations-manager` | Operations Manager |
| `agency-orchestrator` | Agency Orchestrator |
| `agency-program-manager` | Program Manager |
| `agency-project-manager` | Project Manager |
| `agency-release-manager` | Release Manager |
| `agency-scrum-master` | Scrum Master |
| `agency-technical-lead` | Technical Lead |
| `agency-traffic-manager` | Traffic Manager |

### Engineering

| Profile | Role |
|---|---|
| `agency-ai-engineer` | AI Engineer |
| `agency-automation-engineer` | Automation Engineer |
| `agency-backend-engineer` | Backend Engineer |
| `agency-data-engineer` | Data Engineer |
| `agency-database-engineer` | Database Engineer |
| `agency-desktop-application-engineer` | Desktop Application Engineer |
| `agency-devops-engineer` | DevOps Engineer |
| `agency-distributed-systems-engineer` | Distributed Systems Engineer |
| `agency-frontend-engineer` | Frontend Engineer |
| `agency-fullstack-engineer` | Full-Stack Engineer |
| `agency-git-steward` | Git Steward |
| `agency-godot-engineer` | Godot Engineer |
| `agency-infrastructure-engineer` | Infrastructure Engineer |
| `agency-integration-engineer` | Integration Engineer |
| `agency-mlops-engineer` | MLOps Engineer |
| `agency-mobile-engineer` | Mobile Engineer |
| `agency-open-source-maintainer` | Open Source Maintainer |
| `agency-performance-engineer` | Performance Engineer |
| `agency-platform-engineer` | Platform Engineer |
| `agency-privacy-engineer` | Privacy Engineer |
| `agency-security-engineer` | Security Engineer |
| `agency-security-operations-engineer` | Security Operations Engineer |
| `agency-site-reliability-engineer` | Site Reliability Engineer |
| `agency-software-architect` | Software Architect |
| `agency-systems-architect` | Systems Architect |
| `agency-tools-engineer` | Tools Engineer |

### Quality & Review

| Profile | Role |
|---|---|
| `agency-accessibility-reviewer` | Accessibility Reviewer |
| `agency-code-reviewer` | Code Reviewer |
| `agency-compliance-reviewer` | Compliance Reviewer |
| `agency-design-reviewer` | Design Reviewer |
| `agency-qa-automation-engineer` | QA Automation Engineer |
| `agency-qa-lead` | QA Lead |
| `agency-qa-tester` | QA Tester |
| `agency-red-team` | Red Team |
| `agency-security-reviewer` | Security Reviewer |

### Design & Creative

| Profile | Role |
|---|---|
| `agency-art-director` | Art Director |
| `agency-asset-artist` | Asset Artist |
| `agency-audio-designer` | Audio Designer |
| `agency-brand-designer` | Brand Designer |
| `agency-content-designer` | Content Designer |
| `agency-creative-director` | Creative Director |
| `agency-design-systems-designer` | Design Systems Designer |
| `agency-environment-artist` | Environment Artist |
| `agency-graphic-designer` | Graphic Designer |
| `agency-level-designer` | Level Designer |
| `agency-motion-designer` | Motion Designer |
| `agency-narrative-designer` | Narrative Designer |
| `agency-product-designer` | Product Designer |
| `agency-service-designer` | Service Designer |
| `agency-technical-artist` | Technical Artist |
| `agency-ui-ux-designer` | UI/UX Designer |
| `agency-video-producer` | Video Producer |
| `agency-worldbuilder` | Worldbuilder |

### Product & Research

| Profile | Role |
|---|---|
| `agency-business-analyst` | Business Analyst |
| `agency-competitive-analyst` | Competitive Analyst |
| `agency-data-scientist` | Data Scientist |
| `agency-game-designer` | Game Designer |
| `agency-launch-manager` | Launch Manager |
| `agency-market-researcher` | Market Researcher |
| `agency-monetization-strategist` | Monetization Strategist |
| `agency-onboarding-specialist` | Onboarding Specialist |
| `agency-product-manager` | Product Manager |
| `agency-product-operations-manager` | Product Operations Manager |
| `agency-product-strategist` | Product Strategist |
| `agency-requirements-analyst` | Requirements Analyst |
| `agency-research-analyst` | Research Analyst |
| `agency-user-researcher` | User Researcher |

### Marketing & Growth

| Profile | Role |
|---|---|
| `agency-analytics-specialist` | Analytics Specialist |
| `agency-community-manager` | Community Manager |
| `agency-developer-relations-engineer` | Developer Relations Engineer |
| `agency-email-marketer` | Email Marketer |
| `agency-growth-marketer` | Growth Marketer |
| `agency-marketing-strategist` | Marketing Strategist |
| `agency-partnerships-manager` | Partnerships Manager |
| `agency-product-marketing-manager` | Product Marketing Manager |
| `agency-public-relations` | Public Relations |
| `agency-revenue-operations-manager` | Revenue Operations Manager |
| `agency-seo-specialist` | SEO Specialist |
| `agency-social-media-manager` | Social Media Manager |

### Content & Editorial

| Profile | Role |
|---|---|
| `agency-content-writer` | Content Writer |
| `agency-copywriter` | Copywriter |
| `agency-dialogue-writer` | Dialogue Writer |
| `agency-docs-writer` | Documentation Writer |
| `agency-editor-in-chief` | Editor in Chief |
| `agency-localization-specialist` | Localization Specialist |
| `agency-lore-writer` | Lore Writer |
| `agency-release-notes-writer` | Release Notes Writer |
| `agency-scriptwriter` | Scriptwriter |
| `agency-technical-writer` | Technical Writer |

### Operations & Support

| Profile | Role |
|---|---|
| `agency-customer-success` | Customer Success |
| `agency-finance-ops` | Finance Operations |
| `agency-knowledge-manager` | Knowledge Manager |
| `agency-legal-ops` | Legal Operations |
| `agency-people-operations-manager` | People Operations Manager |
| `agency-procurement-specialist` | Procurement Specialist |
| `agency-solutions-engineer` | Solutions Engineer |
| `agency-support-specialist` | Support Specialist |
| `agency-technical-support-engineer` | Technical Support Engineer |
| `agency-training-specialist` | Training Specialist |

The machine-readable roster, categories, and profile names are maintained in [`agency.json`](./agency.json). Routing descriptions live with each profile in its `distribution.yaml`.

## How profiles are structured

Each profile lives under `profiles/<profile-name>/` and is a self-contained Hermes profile distribution:

```text
profiles/
└── agency-backend-engineer/
    ├── distribution.yaml
    ├── SOUL.md
    └── skills/
        └── backend-service-implementation/
            └── SKILL.md
```

`distribution.yaml` contains distribution metadata and the routing description.

`SOUL.md` defines the role's responsibilities, authority, operating standards, collaboration behavior, communication standard, and definition of done.

`skills/` contains the professional procedures bundled with that profile. Skills may also contain supporting references or scripts when the procedure requires them.

A profile may include additional Hermes configuration when the specialty benefits from an intentional capability boundary. The Agency Orchestrator includes a focused Hermes configuration for coordination work.

## Repository layout

```text
.
├── README.md
├── AGENCY.md
├── AGENTS.md
├── agency.json
├── install.py
└── profiles/
```

- `README.md` provides installation and usage documentation.
- `AGENCY.md` defines the shared operating model used across the profile pack.
- `AGENTS.md` contains repository contribution instructions for coding agents and maintainers.
- `agency.json` is the roster used by the installer.
- `install.py` installs all, selected, or category-scoped profiles.
- `profiles/` contains the Hermes profile distributions and their bundled skills.

## Operating model

Profiles are routed by responsibility and ownership. Complex tasks can move through several specialists, with each profile responsible for a bounded part of the work.

A typical software delivery flow might involve:

```text
Product Manager
      ↓
Technical Lead / Architect
      ↓
Implementation Specialists
      ↓
Code Review / QA / Security
      ↓
Git Steward / Release Manager
```

A typical public launch might involve:

```text
Product Manager
      ↓
Launch Manager
      ↓
Marketing Strategist
      ↓
Copy / Content / Social / Brand
      ↓
Analytics / Customer Success
```

See [`AGENCY.md`](./AGENCY.md) for the full collaboration contract.

## Contributing

Profile changes should improve specialization, routing clarity, professional judgment, collaboration quality, or the specialist's bundled skills.

When adding a profile, make sure the role represents a meaningful specialization with work that can be routed to it unambiguously. Add the profile to `agency.json` in the same change and include at least one useful role-specific skill.

See [`AGENTS.md`](./AGENTS.md) for repository-specific contribution rules.

## License

Hermes Agency is licensed under the GNU Affero General Public License v3.0. See [`LICENSE`](./LICENSE).
