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

Use this process for frontend workflow changes, architecture or stack migrations, new external integrations, feature families that add conventions, or replacement of an existing implementation model. Synchronize durable project context before changing source code.

### Required Sequence

1. **Create the root worktree before planning.** Use a dedicated branch and a worktree under `worktree/`. If the current branch is the default branch, create a feature branch first. Do all task edits there. Subagents inherit this worktree and must not create their own.
2. **Check the docs submodule when documentation is in scope.** Inspect `git submodule status docs`; never edit an uninitialized path. Use a docs worktree/branch at the root worktree's exact gitlink and verify `git -C <root-worktree> rev-parse :docs` equals the docs worktree `HEAD`. Commit wiki content separately, then update the root gitlink. A root commit that references a wiki commit must not be published before that wiki commit is available remotely.
3. **Synchronize decision context before implementation.** Create or revise an ADR in `docs/adr/` and update `docs/workflow-governance.md`, `AGENTS.md`, and relevant skills when the workflow changes. Keep the ADR concise and record scope, constraints, tradeoffs, rollout, and rollback.
4. **Track multi-step work.** Before source edits, create `odd/tasks/<feature>.md` and its Engram mirror for large work. Each task line records its spec, route, status, allowed repository-relative `paths`, and commit evidence. Keep exactly one task `in_progress`; for feature branches, the branch suffix matches the task-file name so the commit guard can find it.
5. **Implement and verify.** Use TDD for deterministic behavior changes. Run the applicable grouped Make targets: `make format` for type inference, Ruff fixes/formatting and Pyright; `make pytest` for tests with coverage; and `make cs` for security scans.
6. **Finalize operational docs after verification.** Update user-facing docs and the root `CHANGELOG.md` with verified facts before the relevant commit. ADR and governance context are the pre-implementation exception.
7. **Commit only one approved work unit at a time.** Implementation authorization does not authorize commits. Before every commit, show the exact staged paths, diff summary, and message, then wait for explicit user approval for that individual commit. Stage only paths declared for the active task; do not use `git add -A`. Keep each commit to one task and at most 400 changed diff lines (additions plus deletions), splitting larger work by behavior. Include exactly one matching `Work-Unit: <feature>/<task-id>` trailer in the commit message. Install the root hooks with `make git-hooks`; they validate task scope, size, and the trailer but do not grant approval. Do not bypass a failed hook with `--no-verify`. Record the resulting hash in the task file. Push, PR, merge, deployment, and release require separate authorization.

### Non-Negotiable Rules

- Any workflow or stack migration requires an ADR before implementation.
- Any new integration that changes project conventions must update both `AGENTS.md` and the relevant `SKILL.md`.
- Skills must stay concise and use progressive disclosure; put detailed procedures in focused docs and reference them.
- If a file becomes stale after a migration, update it in the same change rather than leaving conflicting instructions behind.

## Documentation and Verification

- Before creating a file, check chat and the repository for duplicate content. Do not copy the conversation into documentation. Required ADRs, workflow records, and large-task specs are durable repository artifacts; keep them concise and record only project policy/evidence not already captured elsewhere. Add `chat_decisions_checked: "YES"` or `"NO"` metadata to new governance artifacts.
- Run `make format`, `make pytest`, and `make cs` as applicable; document any pre-existing failures accurately. Use a browser check for UI changes, not for unrelated backend or workflow changes.
- Update user-facing documentation and `CHANGELOG.md` after verification and before the corresponding commit.
- Install the root Git hooks with `make git-hooks`. The pre-commit hook rejects staged paths outside the active task's declared `paths` and more than 400 changed lines. The commit-msg hook requires the matching `Work-Unit: <feature>/<task-id>` trailer. These local hooks are safeguards and can be bypassed; they never replace explicit user approval.

## Commit Approval

- Before **each** `git commit`, present its exact staged paths, diff summary, and commit message, and wait for explicit approval of that commit. Approval of implementation or of a previous commit does not carry over.
- If a hook changes the index or working tree, inspect and stage the final diff again; any changed commit scope requires fresh approval.
- Never create a combined end-of-feature commit from multiple completed tasks. Never push or create a PR unless separately authorized.

## Key Files
| File | Purpose |
|------|---------|
| `AGENTS.md` | Agent configuration |
| `docs/workflow-governance.md` | Change process |
| `docs/PDR/` | Roadmap |
| `.atl/skill-registry.md` | Skill index |
| `Makefile` | Build entry point |
