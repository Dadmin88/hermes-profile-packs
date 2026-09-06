---
name: profile-pack-authoring
description: Author approved portable Hermes profile distributions.
---
# Profile Pack Authoring

Use when creating or materially revising a portable profile distribution in a Hermes Profile Packs repository. This procedure produces repository source artifacts only; it never creates or edits an installed profile in a live Hermes home.

## When to use

- A human requests a new professional, personal, or teaching profile for an existing pack.
- An existing profile needs a material role, SOUL, skill-set, metadata, or routing-boundary revision.
- A third-party profile or skill provides useful methods that must be reviewed, adapted, attributed, and vendored safely.

Do not use for installing profiles, changing live Hermes configuration, coordinating a project team, building a general-purpose profile generator, or creating another BotFather/Botmaker/profile-factory role.

## Required inputs

Before writing a new profile directory, establish:

1. Owning pack and namespace.
2. Stable distribution identity and display name.
3. One-sentence durable responsibility and expected deliverables.
4. Explicit authority boundaries and a not-list.
5. Neighboring profiles whose ownership could be confused with the proposal.
6. Initial role-specific skill set.
7. Human approval of items 1-6. An approved task specification or a human sign-off on the specific draft satisfies this gate.

If the responsibility still contains unrelated jobs or the boundary cannot be routed reliably, stop at the proposal and ask one focused question. Do not materialize a catch-all profile.

## Procedure

### 1. Inspect the repository contract

- Read the repository and pack-level instruction files, pack specification, manifest, validator, relevant tests, README roster, changelog, and two or more neighboring profile distributions.
- Trace how the manifest, installer, catalog, routing evaluations, and documentation derive or assert profile metadata.
- Check the working tree before editing and preserve unrelated changes.

Complete this step only when the exact required artifact set, category, release version, and validation commands are known from repository evidence.

### 2. Sharpen and approve the role

Draft a compact proposal containing the identity, display name, category, one-sentence responsibility, owned deliverables, not-list, collaborators, and initial skill names. Compare it explicitly with each neighboring specialty.

Do not create the profile directory or publish a roster entry until the human approves this concrete proposal. Treat a signed task card as approval only for decisions it actually fixes; surface any material gap rather than guessing.

Complete this step when one durable owner and the adjacent handoff boundaries are unambiguous.

### 3. Review external inspiration safely

When adapting third-party material:

- inspect the canonical repository at the pinned revision, including instructions, scripts, references, install behavior, and license;
- reject secret discovery, credential copying, persistence, mutable downloads, unnecessary broad filesystem access, safeguard bypasses, or host-specific runtime assumptions;
- preserve only methods that fit Profile Packs, rewriting tool- or site-specific mechanics rather than copying them blindly;
- add a local `SOURCE.md` with canonical source, source path, reviewed revision, review date, upstream author, license, adaptations, excluded material, and the required license notice.

Complete this step when every reused concept is attributable, permitted, portable, and scoped.

### 4. Draft the distribution before the roster

Create the approved repository-relative distribution directory using the owning pack's established layout. At minimum include:

- `distribution.yaml` with identity, pack release version, clear routing description, author, and license;
- `SOUL.md` with role, responsibilities, authority boundaries, working standard, collaborators, communication, and definition of done;
- at least one focused `skills/<skill>/SKILL.md` containing a repeatable procedure and quality gate;
- `.no-bundled-skills` only when the approved profile intentionally excludes unrelated default skills and pack conventions permit the marker;
- supporting references or scripts only when they materially improve reliable execution.

Do not add model/provider pins, credentials, memories, runtime databases, logs, sessions, local absolute paths, host identifiers, live presence, or placement behavior. Do not alter protected-instruction or approval safeguards.

Keep identity and durable behavior in the SOUL. Put commands, checklists, validation sequences, and reusable methods in skills. Complete this step when the profile can be reviewed as a standalone portable distribution.

### 5. Prove routing boundaries

Write a routing description that names the work and deliverables rather than generic traits. Compare it with neighboring profiles and add deterministic routing evaluation cases when a reasonable request could select the wrong owner.

Include one positive ownership case and enough negative boundary cases to distinguish the new role from adjacent specialties. A multi-role request belongs to the pack's coordinator; application implementation belongs to its implementing specialist; repository governance belongs to its maintainer.

Complete this step when representative requests map to one justified owner without relying on roster order.

### 6. Publish metadata and documentation

Only after the distribution and role-specific skill are complete:

- insert the profile in the manifest's established deterministic order;
- update declared profile and category counts from the resulting roster;
- update pack and root documentation totals and roster tables;
- update any other current documentation that states the old all-pack total;
- add a concise changelog entry describing the shipped capability and provenance.

Do not add the role to a routing backbone unless the product decision explicitly makes it core infrastructure. Complete this step when every public count and roster representation agrees with the source tree.

### 7. Add focused regression coverage

Extend tests or validators for new invariants that generic pack validation does not prove. Prefer behavior and contract assertions over snapshots of incidental prose.

For a profile-authoring specialist, protect at least: stable identity/category, required focused skill, isolation marker if approved, absence of model/provider and safeguard overrides, preserved source revision/license notice, and routing boundaries against adjacent roles.

Complete this step when a regression in a material product constraint fails an automated check.

### 8. Validate and hand off

Run every validation command required by the repository instructions, not only the pack-local suite. Also run the pack catalog or dry-run surface when local instructions require it. Inspect the final diff and working-tree status for unrelated changes, generated state, secrets, local paths, inconsistent counts, and malformed metadata.

Do not commit, push, install, or modify a live profile. Hand runtime actions to their owning specialist, then hand off the changed files, exact command results, provenance, material risks, and next certification/review action.

## Quality gate

A profile is ready for review when its responsibility is singular and approved; the SOUL and skills are separated correctly; routing language distinguishes adjacent roles; distribution metadata, roster, counts, docs, and evals agree; external inspiration is pinned and attributed; no live state, secret, local path, model/provider pin, safeguard override, or recursive profile factory is present; and every required validator and test passes.