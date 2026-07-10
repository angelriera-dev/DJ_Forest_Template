---
name: django-fortress-saas
description: >
  Security-first Django 6.x SaaS monolith.
version: "1.0"
---

# Django Fortress SaaS — Agent Configuration

## Project Overview

**Django Fortress** is a security-first SaaS boilerplate implementing OWASP Top 10 2026 standards natively.

## Methodological Approach: Secure by Design + TDD

**TDD (Mandatory):**

- Every new feature follows the **Red → Green → Refactor** cycle.
- Cover models, business services (SRS logic), views, and validation/comparison logic.
- Use `pytest-django`.
- Integration tests for the entire <app_name> workflow.
- High coverage (>85% in critical logic). Tests **must always pass** before merging.
- Security tests (ownership properties, input validation, rate limits).

## Standards & Methodology
**General methodology:** Short iterations (1–2 weeks), focus on the **core loop** of the <app_name> from the very first weeks.

## Template Integration (Surgical Workflow)

Any integration with the `template` remote (contributions or syncs) MUST use the **Surgical Integration Workflow**.

- **Rule**: Never use standard git merge/squash for template contributions.
- **Protocol**: 
  1. Create a branch from `template/main`.
  2. Use `scripts/template-contribute.sh` to stage only intended files.
  3. Validate with `scripts/template-pr-check.sh` before pushing.
- **Reference**: See `SKILLS/local-architecture-templates/SKILL.md` for the full procedure.

## Tech Stack
| Layer | Technology |
|-------|------------|
| Backend | Django 6.x |
| Auth | django-allauth |
| Frontend | HTMX + Alpine.js + Tailwind + DaisyUI |
| Testing | pytest-django |
| Quality | Ruff, Pyright, Bandit, Semgrep |

## Critical Path Facts
- `BASE_DIR` = `src/`
- `STATICFILES_DIRS` = `src/static/`
- `TEMPLATES_DIRS` = `src/templates/`
- `src/config/settings/` is a Python package — read specific files (`base.py`, `core/*.py`).

### Adding New Routes

1. **Standard views**: Add to `<app>/urls.py` and `<app>/views.py`
2. **HTMX partials**: Add to `<app>/api/urls.py` and `<app>/api/views.py`
3. **REST endpoints**: Add versioned route to `<app>/api/urls.py` with `v1/` prefix
4. **New API version**: Create new `v2/` prefix in `<app>/api/urls.py` when needed

### Naming Conventions

- Standard views: `<app>:<action>` (e.g., `<app_name>:page_home`, `dashboard:settings`)
- API routes: `api:<app>:<resource>` (e.g., `api:<app_name>:action`)
- Use underscores, not hyphens, in URL names
- Prefix API names with `api_` when they return JSON

For detailed routing patterns and examples, see `docs/adr/ADR-routing-convention.md`.

## Available Local Skills

Consult `.atl/skill-registry.md` for more information about skills.

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

1. **Create/Switch Worktree**
   - Before any planning, create a dedicated Git worktree for the task if one does not exist (e.g., `git worktree add ../<task-name> <branch-name>`).
   - All subsequent work MUST be performed within this worktree.
2. **Write or update an ADR**
   - Create or revise a file in `docs/adr/`.
   - Record scope, motivation, constraints, tradeoffs, rollout, and rollback.
3. **TDD + Secure by Design**
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

1.  **Technical Validation**:
    - Run `make check_code` to execute the full quality suite (lint, type-check, tests, Django checks).
    - All checks MUST pass (clean exit). If there are existing errors, they must be addressed or explicitly documented as "pre-existing" in the PR.
2.  **Functional Verification**:
    - Manually verify the affected feature/view in the browser.
3.  **User Acceptance**:
    - Present the changes to the user with evidence (logs/screenshots if possible).
    - Ask: "Please verify the changes in your browser. Is everything behaving correctly?"


## Pre-Commit Workflow
1. Run `make check_code && make test`.
2. Commit with conventional format.
3. Update `CHANGELOG.md`.
4. Create PR.

## Source-of-Truth Hierarchy
1. Explicit user request
2. `AGENTS.md`
3. `docs/adr/`
4. Active `SKILL.md` instructions
5. `docs/workflow-governance.md`

## Key Files
| File | Purpose |
|------|---------|
| `AGENTS.md` | Agent configuration |
| `docs/workflow-governance.md` | Change process |
| `docs/PDR/` | Roadmap |
| `.atl/skill-registry.md` | Skill index |
| `Makefile` | Build entry point |
