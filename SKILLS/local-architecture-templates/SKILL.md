---
name: local-architecture-templates
description: >
  Use this skill when editing files in templates/ or defining component,
  rendering, or styling conventions for the template layer of this repository.
  It explains the local architecture, boundaries, and reusable patterns specific
  to the templates/ area of this project.
license: MIT
metadata:
  author: rag
  version: "2.2"
---

## When to Use

Use this skill when:
- Creating or modifying templates in `templates/`
- Adding or refactoring reusable components in `templates/components/`
- Applying folder-specific rendering and styling conventions
- Updating template architecture for this repository

If the task changes the rendering model, shared component structure, or frontend workflow, follow `docs/workflow-governance.md` first.

## Local Scope

- Primary folder: `templates/`
- Shared components: `templates/components/`
- Related workflow rules: `docs/workflow-governance.md`

## Current Stack Context

- Django templates
- HTMX
- Alpine.js
- Tailwind CSS
- DaisyUI

Use `SKILLS/django-htmx/SKILL.md` for cross-project HTMX and Alpine patterns.

## Local Conventions

1. Prefer reusable components from `templates/components/`.
2. Keep template conventions local to the `templates/` architecture skill.
3. Prefer DaisyUI and Tailwind utilities over custom CSS where possible.
4. Escalate workflow or rendering-model changes through ADR + governance first.
5. **App Isolation (Vertical Architecture)**: Apps must encapsulate their own app-specific styles, scripts, templates, and view transitions. Never pollute global stylesheets (`src/static/css/styles.css`) or global scripts (`src/static/js/alpine_init.js`) with app-specific transitions or selector logic. If an app is removed, it must leave zero orphan assets behind. Place app-specific assets under `src/apps/<app_name>/static/<app_name>/` and load them modularly inside the app's base templates.

## Default Procedure

1. Identify the template or component scope.
2. Reuse existing components before adding new ones.
3. Apply project-local naming and structure conventions.
4. Update related documentation if the convention changes.
5. Run validation commands required by `AGENTS.md` when the change affects behavior.

## Template Upstream Workflow (two directions)

The repo tracks an upstream SaaS template as the `template` remote
(`https://github.com/angelriera-dev/Sass_Forest_Bolier.git`). Both directions
must keep `template/main` history clean — never mix `origin` history into a
template PR.

### 1. Pull updates FROM template (Extensible mode)

`make template-sync` creates `update-template` from `template/main` and
`--squash` merges it, so upstream changes land as one squashed commit without
importing template's history.

### 2. Contribute TO template (reverse PR)

Goal: a clean PR against `template/main` containing only the files you choose,
following template's history (not origin's).

- Branch MUST start from `template/main`, never from an `origin` branch — that
  is what keeps the PR diff scoped to your contribution.
- Select files selectively: bring them from your current commit with
  `git checkout <src> -- <path>` (whole file) or
  `git restore --source=<src> --patch -- <path>` (hunks).
- Commit in controlled, well-scoped commits; then push the branch to the
  `template` remote and open the PR.

Helpers (in `scripts/`):

- `scripts/template-diff.sh` — list files that differ between current HEAD and
  `template/main` (candidates to contribute).
- `scripts/template-contribute.sh <branch> [file ...]` — create a clean branch
  from `template/main` and stage the given files from the current commit.

`make template-contribute` / `make template-contribute-push` wrap the same
flow from the Makefile.

### Rules

- **Always work in a dedicated branch. Never merge or push to `main` on either
  remote (`origin` or `template`).** Creating a separate branch before any
  cross-remote operation is mandatory — it protects both projects from lost or
  entangled work.
- Never push `origin` branches or their full history to the `template` remote.
- Only contribute template-relevant assets (shared components, base layout,
  theming). Keep app-specific code out of a template PR.
- Each contribution PR must be a single logical change with a clean commit.
- Run `scripts/template-pr-check.sh` before pushing. It aborts the PR if the
  diff against `template/main` contains forbidden files (app code, secrets,
  media, local data).

### Integrity protocol (hypothetical template PR)

1. **Isolate**: stay on your feature branch; never touch `origin/main`.
   Create the contribution branch from `template/main`
   (`scripts/template-contribute.sh <branch> [files]`), so origin history is
   excluded and `origin` stays untouched.
2. **Select**: stage ONLY template-relevant, shareable files. Exclude
   `src/apps/`, `.env*`, `src/media/`, `*.sqlite3`, secrets, local settings,
   migrations specific to this project.
3. **Verify**: `scripts/template-pr-check.sh` — aborts on forbidden paths;
   then `git diff template/main...HEAD` to eyeball every hunk.
4. **Commit**: one controlled, conventional commit scoped to the template change.
5. **Push safely**: `git push template <branch>` (never `--force` to `main`).
6. **Open PR**: base = `template/main`; head = your branch.
7. **Cleanup**: after merge, delete the branch locally and on `template`;
   `git fetch template` to refresh; resume work on `origin` normally.

## Reference
- `AGENTS.md`
- `docs/workflow-governance.md`
- `SKILLS/django-htmx/SKILL.md`
- `CHANGELOG.md`
- `Makefile` (`template-sync`, `template-contribute`, `template-contribute-push`)
- `SKILLS/local-architecture-templates/scripts/`
