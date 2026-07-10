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

## Methodological Approach: Secure by Design + TDD

**TDD (Mandatory):**

- Every new feature follows the **Red → Green → Refactor** cycle.
- Cover models, business services (SRS logic), views, and validation/comparison logic.
- Use `pytest-django`.
- Integration tests for the entire <app_name> workflow.
- High coverage (>85% in critical logic). Tests **must always pass** before merging.
- Security tests (ownership properties, input validation, rate limits).

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
| Frontend | HTMX + Alpine.js |
| CSS | Tailwind CSS + DaisyUI |
| DB | SQLite (dev) / PostgreSQL (prod) |
| Testing | pytest-django (Strict TDD) |
| Quality | Ruff, Pyright, Bandit, Semgrep |

## Project Structure

```
src/                        # ← BASE_DIR resolves here (not the repo root)
├── apps/
│   ├── users/              # User management + allauth
│   ├── dashboard/          # Main app views
│   └── <app_name>/              # <app_name> app with SRS
│       ├── urls.py         # Standard views (full-page HTML)
│       ├── views.py        # Standard view logic
│       ├── api/            # API routes (versioned)
│       │   ├── urls.py     # API URL patterns (v1, v2, etc.)
│       │   └── views.py    # HTMX partials + REST endpoints
│       ├── templates/      # App-specific templates
│       └── tests/          # Test suite
├── static/                 # STATICFILES_DIRS points here → /static/ URL
│   ├── css/styles.css      # Project-specific styles (not CDN)
│   └── js/
│       ├── theme.js        # Theme bootstrap — no defer, no Alpine dependency
│       └── alpine_init.js  # Alpine.data() registrations only
├── templates/              # TEMPLATES DIRS points here
│   ├── components/
│   │   ├── cdns.html       # ALL external CDNs: Tailwind, DaisyUI, HTMX, Alpine
│   │   └── Layout/
│   │       └── navbar.html # Theme toggle lives here (daisyUI theme-controller)
│   ├── account/            # allauth templates
├── config/                 # Django config package — settings/ is a DIRECTORY
│   ├── urls.py             # Main URL configuration
│   └── settings/           # Modular settings — read individual files, not the folder
│       ├── base.py         # Core settings + INSTALLED_APPS + TEMPLATES
│       ├── dev.py          # Development overrides
│       ├── prod.py         # Production overrides
│       └── core/
│           ├── storage.py  # STATIC_URL, STATICFILES_DIRS, MEDIA_ROOT
│           ├── security.py # Security headers, HTTPS settings
│           └── database.py # DB config
├── docs/
│   ├── PDR/                # Product Requirements Document
│   └── adr/                # Architecture Decision Records
├── AGENTS.md               # This file
├── CHANGELOG.md            # Change log
├── Makefile                # Build entry point
└── requirements.txt
```

### Critical path facts

- `BASE_DIR` = `src/` — all relative paths start here, not from the repo root
- `STATICFILES_DIRS = [BASE_DIR / "static"]` → physical: `src/static/`, URL: `/static/`
- `TEMPLATES DIRS = [BASE_DIR / "templates"]` → `src/templates/`
- `src/config/settings/` is a **directory** (Python package), not a file — always read specific files inside it (`base.py`, `core/storage.py`, etc.)
- `src/media/` is for user-uploaded files (MEDIA_ROOT), not static assets

## Frontend Conventions

### Static files

- Assets go in `src/static/` — never inside `src/templates/`
- Use `{% load static %}` + `{% static 'path' %}` in templates — never hardcode `/static/` paths
- `src/templates/components/cdns.html` contains **all** external CDNs (Tailwind, DaisyUI, HTMX, Alpine) — do not delete or split it

### JS loading order (critical)

The order in `base.html` is intentional and must be preserved:

```html
<script src="{% static 'js/theme.js' %}"></script>       {# no defer — runs before first paint #}
{% include "components/cdns.html" %}                      {# CDNs including Alpine #}
<script src="{% static 'js/alpine_init.js' %}" defer></script>  {# defer — registers before Alpine boots #}
```

- `theme.js` — IIFE, no Alpine dependency, no defer. Applies theme and color variables before paint.
- `alpine_init.js` — registers `Alpine.data()` components by listening to `alpine:init`. Must load with `defer` so it races correctly with the Alpine CDN. **Never** put theme logic here.
- Mixing theming into `alpine_init.js` causes `app is not defined` errors on navigation and cross-browser failures because Alpine may boot before the script executes.

### Theming

- Light/dark toggle uses daisyUI's native `theme-controller` (CSS only, no Alpine):
  ```html
  <label class="swap swap-rotate">
    <input type="checkbox" class="theme-controller" value="dark" />
    ...
  </label>
  ```
- Custom color variables (`--color-primary`, `--color-secondary`, `--color-accent`) are set via `document.documentElement.style.setProperty()` and persisted in `localStorage` — no build step needed.
- `theme.js` restores both the light/dark state and any custom color variables on every page load.
- Do **not** use Alpine `$watch`, `toggleTheme()`, or `x-data` for theming.

### settings/ is a directory, not a file

`src/config/settings/` is a Python package. Always read specific files:
- `src/config/settings/base.py` — INSTALLED_APPS, TEMPLATES, MIDDLEWARE
- `src/config/settings/core/storage.py` — STATIC_URL, STATICFILES_DIRS, MEDIA_ROOT
- `src/config/settings/core/security.py` — security headers
- `src/config/settings/dev.py` / `prod.py` — environment overrides

Never attempt to read or cat `src/config/settings/` as if it were a file.

## Routing Conventions

### URL Structure

The project uses a two-tier routing system:

1. **Standard Views** (`/<prefix>/`): Full-page HTML responses for client-side navigation
2. **API Routes** (`/api/`): Versioned endpoints for HTMX partials and REST APIs

### Route Categories

#### Standard Views (`app/urls.py`)
- Mounted at a descriptive prefix (e.g., `/dashboard/`, `/app/`)
- Serve complete HTML pages
- HTMX-compatible (return partials when HX-Request header present)
- Examples: Home dashboard, page initialization

#### API Routes (`app/api/urls.py`)
- Mounted at `/api/<app>/` in main URL config
- Two sub-categories:

**HTMX Partials** (prefix `hx_` conceptually):
- Return HTML fragments for HTMX `hx-get`/`hx-post` targets
- Session-dependent state management
- Examples: Carousel navigation, CRUD operations

**REST Endpoints** (prefix `rest` conceptually):
- Return `JsonResponse` for API consumers
- Versioned path prefix (`v1/`, `v2/`, etc.)
- Authentication required
- Examples: Resource list endpoint

### Versioning Strategy

API routes use path-based versioning:
- Current: `/api/<app>/v1/<resource>/`
- Future: `/api/<app>/v2/<resource>/` for breaking changes
- Version prefix defined in `app/api/urls.py` `urlpatterns`

### Adding New Routes

1. **Standard views**: Add to `app/urls.py` and `app/views.py`
2. **HTMX partials**: Add to `app/api/urls.py` and `app/api/views.py`
3. **REST endpoints**: Add versioned route to `app/api/urls.py` with `v1/` prefix
4. **New API version**: Create new `v2/` prefix in `app/api/urls.py` when needed

### Naming Conventions

- Standard views: `<app>:<action>` (e.g., `<app_name>:page_home`, `dashboard:settings`)
- API routes: `<app>:api_<resource>` (e.g., `<app_name>:api_action`)
- Use underscores, not hyphens, in URL names
- Prefix API names with `api_` when they return JSON

### Reference

For detailed routing patterns and examples, see `docs/adr/ADR-routing-convention.md`.

## Available Skills

| Skill | Trigger | Location |
|-------|---------|----------|
| **local-architecture-docs** | Editing `docs/`, ADRs, governance, documentation indexes | `SKILLS/local-architecture-docs/SKILL.md` |
| **local-architecture-routing** | Creating/modifying URL patterns, API routes, versioning | `SKILLS/local-architecture-routing/SKILL.md` |
| **local-architecture-templates** | Modifying `templates/`, components, and template conventions | `SKILLS/local-architecture-templates/SKILL.md` |
| **saas-workflow** | Managing template upstream, syncing, or SaaS project initialization | `SKILLS/saas-workflow/SKILL.md` |
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
4. **TDD + Secure by Design**
5. **Update the formal process document**
   - Keep `docs/workflow-governance.md` aligned with the required sequence and checklists.
6. **Record the change**
   - Add a `CHANGELOG.md` entry summarizing the governance update and affected files.
7. **Only then implement**
   - Make code or template changes after the context and instructions are synchronized.
8. **Validate**
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
