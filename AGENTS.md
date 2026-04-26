---
name: django-fortress-saas
description: >
  Security-first Django 6.x SaaS monolith with HTMX, Alpine.js, Tailwind CSS, and DaisyUI.
  Reference implementation of OWASP Top 10 2026 mitigations with modular, tested architecture.
version: "1.0"
---

# Django Fortress SaaS — Agent Configuration

## Project Overview

**Django Fortress** is a security-first SaaS boilerplate implementing OWASP Top 10 2026 standards natively.
While AI can generate code, developers own data integrity and architectural security.
This project provides a production-ready, audited foundation with zero shortcuts.

**Current Phase**: Phase 1 (Foundations & Hardening) — See `docs/PDR/` for full 6-phase roadmap.

## Development Standards

- Deliver small, correct, validated, and verifiable changes
- Security by default: OWASP mitigations are non-negotiable
- Test-driven: strict pytest-django mode active; 90%+ coverage required
- Educational: every decision backed by ADR explaining the "why"
- English-only output from agents
- Treat `AGENTS.md` as living agent documentation; update it when project workflow or conventions change

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 6.x |
| Auth | django-allauth |
| Frontend | HTMX + Alpine.js |
| CSS | Tailwind CSS + DaisyUI |
| DB | SQLite (dev) / PostgreSQL (prod) |
| Testing | pytest-django (Strict TDD) |
| Quality | Ruff, Pyright, Bandit, Semgrep |

## Project Structure

```
my_sass/
├── apps/
│   ├── users/          # User management + allauth
│   └── dashboard/      # Main app views
├── templates/
│   ├── components/     # Reusable UI components
│   ├── account/        # allauth templates
│   └── dashboard/      # App templates
├── config/
│   └── settings/       # Django settings (modular hierarchy)
├── docs/
│   ├── PDR/            # Product Requirements Document
│   └── adr/            # Architecture Decision Records
├── AGENTS.md           # This file
├── CHANGELOG.md        # Change log
├── Makefile            # Build entry point
└── requirements.txt
```

## Available Skills

| Skill | Trigger | Location |
|-------|---------|----------|
| **local-architecture-docs** | Editing `docs/`, ADRs, governance, documentation indexes | `SKILLS/local-architecture-docs/SKILL.md` |
| **local-architecture-templates** | Modifying `templates/`, components, and template conventions | `SKILLS/local-architecture-templates/SKILL.md` |
| **django-htmx** (global) | HTMX, Alpine.js, Tailwind patterns | Loaded on-demand |
| **django-allauth** (global) | Authentication, OAuth, MFA | Loaded on-demand |

Global skills cover reusable cross-project technologies.
Local architecture skills cover folder-specific conventions and boundaries inside this repository.

## Source-of-Truth Hierarchy

When instructions overlap, interpret project context in this order:

1. Explicit user request in chat

2. Nearest `AGENTS.md`
3. Relevant ADR in `docs/adr/`
4. Activated `SKILL.md` instructions
5. Supporting project docs such as `docs/*.md`
6. Historical record in `CHANGELOG.md`

`CHANGELOG.md` records what changed; it does not define the active workflow.

## Formal Change Governance

Use this process for any of the following:

- frontend workflow changes
- architecture or stack migrations
- new external integrations
- new feature families that add new patterns or conventions
- replacing an existing implementation model (for example Django components to React CDN islands)

Do **not** jump directly into implementation. Update project context first.

### Required Sequence

1. **Classify the change**
   - Decide whether it is a local implementation detail or a workflow/architecture/integration change.
   - If it changes conventions, folder structure, activation rules, build/test flow, or agent instructions, treat it as governance-impacting.
2. **Write or update an ADR**
   - Create or revise a file in `docs/adr/`.
   - Record scope, motivation, constraints, tradeoffs, rollout, and rollback.
3. **Update agent operating context**
   - Update `AGENTS.md` for stack, commands, structure, and mandatory workflow.
   - Update the relevant `SKILL.md` files for task-specific execution rules.
   - Update `.atl/skill-registry.md` only as a discovery index after the governing files are correct.
4. **Update the formal process document**
   - Keep `docs/workflow-governance.md` aligned with the required sequence and checklists.
5. **Record the change**
   - Add a `CHANGELOG.md` entry summarizing the governance update and affected files.
6. **Only then implement**
   - Make code or template changes after the context and instructions are synchronized.
7. **Validate**
   - Run the relevant checks, at minimum `make test`, `make lint`, and `make type-check` when applicable.

### Non-Negotiable Rules

- Any workflow or stack migration requires an ADR before implementation.
- Any new integration that changes project conventions must update both `AGENTS.md` and the relevant `SKILL.md`.
- Skills must stay concise and use progressive disclosure; put detailed procedures in focused docs and reference them.
- If a file becomes stale after a migration, update it in the same change rather than leaving conflicting instructions behind.


## Avoid redundant files rule

- Purpose: Prevent creating new files that duplicate information or decision-making content already captured in the chat.
- When to apply: Before creating any file for a change, check if the same information or decisions already exist in the chat.
If the content (context, rationale, decisions, or action items) is present in chat, do NOT create a file; keep it in the chat only.
If a file is necessary, include only unique, concise content that is not stored in chat (no duplicate rationale, decisions, or full context).
- File names: use clear, minimal names indicating unique purpose (e.g., "migration-script.sh" — not "decision-notes.txt").
- Verification: Require one explicit check step: "Checked chat for existing decisions: YES/NO" recorded in the file metadata.

## Pre-Commit & Verification Workflow

To ensure code integrity and functional stability, every change MUST follow this verification sequence before finalization and commit:

1.  **Technical Validation**:
    - Run `make check_code` to execute the full quality suite (lint, type-check, tests, Django checks).
    - All checks MUST pass (clean exit). If there are existing errors, they must be addressed or explicitly documented as "pre-existing" in the PR.
2.  **Functional Verification**:
    - Start the development server with `make run`.
    - Manually verify the affected feature/view in the browser.
    - Confirm HTMX interactions and Alpine.js components behave as expected.
3.  **User Acceptance**:
    - Present the changes to the user with evidence (logs/screenshots if possible).
    - Ask: "Please verify the changes in your browser. Is everything behaving correctly?"
4.  **Commit**:
    - Only commit once Technical, Functional, and User validations are successful.
    - Use conventional commit messages.

## Build & Test Commands

- `make install` — Install dependencies
- `make run` — Start development server
- `make test` — Run pytest with coverage
- `make lint` — Run Ruff linter
- `make type-check` — Run Pyright static type checker

## Pre-Commit Workflow

1. Make changes in topic branch
2. Run `make test && make lint && make type-check`
3. If all pass: commit with conventional format — `git add . && git commit -m "type: subject"`
4. Update CHANGELOG.md BEFORE push
5. Create PR for review

## Key Files

| File | Purpose |
|------|---------|
| `AGENTS.md` | This file; agent configuration |
| `docs/workflow-governance.md` | Formal process for workflow, migration, and integration changes |
| `docs/PDR/` | Product Requirements Document; 6-phase roadmap |
| `docs/adr/` | Architecture decisions and migration approvals |
| `.atl/skill-registry.md` | Skill discovery registry (delegator-internal) |
| `CHANGELOG.md` | Timestamped record of all changes |
| `Makefile` | Single point of entry for all commands |

## Reference

- Product Vision: `docs/PDR/PDR.md`
- Phase 1 Details: `docs/PDR/Fase1.md`
- Workflow Governance: `docs/workflow-governance.md`
- Security Standards: `docs/adr/`
- Change History: `CHANGELOG.md`
