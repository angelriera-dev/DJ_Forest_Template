# CHANGELOG

All notable changes to this project are documented here.

Format: `YYYY-MM-DD — Summary — Files Affected`

---

## 2026-04-21 — Rename folder-scoped skills to `lacal_architecture_*` and move them under `SKILLS/`

**Summary**: Adopted a dedicated naming convention for project-local architecture skills so folder-scoped guidance is clearly separated from reusable technology skills. Moved the local documentation and template skills into `SKILLS/`, updated indexes and references, and recorded the policy in a new ADR.

**Files Affected**:
- `docs/adr/ADR-002-local-architecture-skill-naming.md` — Recorded the naming convention and migration plan
- `SKILLS/lacal_architecture_docs/SKILL.md` — New local architecture skill for `docs/`
- `SKILLS/lacal_architecture_templates/SKILL.md` — New local architecture skill for `templates/`
- `AGENTS.md` — Replaced old local skill references with the new convention and clarified global vs local skills
- `.atl/skill-registry.md` — Reindexed skills with a dedicated Local Architecture Skills section
- `SKILLS/README.md` — Updated the human-readable index to the new skill names and paths
- `docs/Home.md` — Replaced stale references with a smaller current documentation index
- `docs/SKILL.md` — Removed old skill entry point
- `templates/SKILL.md` — Removed old skill entry point

## 2026-04-21 — Refactor agent configuration to comply with agents.md + agentskills.io spec

**Summary**: Migrated project configuration from mixed-language, non-compliant structure to standards-compliant English-only format. Removed pre-digested Compact Rules (violates progressive disclosure). Fixed stale path references. Added YAML frontmatter to agent and skill definitions.

**Files Affected**:
- `AGENTS.md` — Added YAML frontmatter, fixed path refs, translated Spanish → English, added build/test commands
- `docs/SKILL.md` — Converted to invocable "Documentation Management" skill, added YAML frontmatter, translated to English
- `templates/SKILL.md` — Updated description, removed broken global skill refs, ensured English output
- `.atl/skill-registry.md` — Removed Compact Rules block, fixed paths (/dj/htmx → /my_sass), translated comments, simplified format
- `CHANGELOG.md` — Created to log all changes going forward

**Spec References**:
- https://agents.md/ — Standard for AGENTS.md files
- https://agentskills.io/specification — Standard for SKILL.md files

**Notes**:
- No code changes; config-only refactoring
- All agent output now English-only
- Progressive disclosure enabled: skills load on-demand, not pre-digested
- Sub-agents discover skills via registry table; full rules load from SKILL.md files

## 2026-04-21 — Register formal workflow governance for migrations, integrations, and new conventions

**Summary**: Added a project-wide formal process for workflow/stack migrations and integration-driven feature changes. Introduced a governance document, recorded the decision as an ADR, and updated agent/skill context so governance updates happen before implementation when conventions change.

**Files Affected**:
- `AGENTS.md` — Added source-of-truth hierarchy and mandatory change-governance sequence
- `docs/workflow-governance.md` — Added formal process, checklists, and ADR template
- `docs/adr/ADR-001-workflow-governance.md` — Recorded the governance decision and rationale
- `docs/Home.md` — Added quick links to the new governance and agent docs
- `docs/SKILL.md` — Added governance-first documentation rules
- `templates/SKILL.md` — Added migration guardrail for template-system changes
- `.atl/skill-registry.md` — Registered governance doc as a project convention resource

---

## 2026-04-22 — Cleanup redundant files and document project tooling

**Summary**: Initiated the `clean-architecture-frontend-automation` change by sanitizing the project environment and establishing a comprehensive AppSec Knowledge Base. Created dedicated documentation for Ruff, Pyright, SAST (Bandit/Semgrep), and automation workflows to serve as an educational wiki. Removed obsolete CDN template and updated git ignore rules.

**Files Affected**:
- `docs/appsec/` — New dedicated folder for security tooling documentation
- `docs/appsec/index.md`, `ruff.md`, `pyright.md`, `sast.md`, `automation.md` — Detailed didactic guides
- `docs/TOOLING.md` — Centralized entry point for quality standards
- `.gitignore` — Added patterns for Python cache, pytest cache, and environment files
- `config/templates/cdns.html` — Deleted redundant file; consolidated in `templates/cdns.html`
- `CHANGELOG.md` — Updated with latest changes

---

## 2026-04-22 — Integrate pre-commit hooks and static security scanners

**Summary**: Hardened the CI/CD pipeline and local development workflow by integrating automated security and quality tools. Added Bandit and Semgrep for SAST scanning, and configured pre-commit hooks to enforce coding standards before every commit. Updated Makefile with dedicated security and cleanup targets.

**Files Affected**:
- `.pre-commit-config.yaml` — New configuration for automated git hooks
- `requirements/local.txt` — Added `bandit`, `semgrep`, and `pre-commit`
- `Makefile` — Added `security_scan`, `clean` targets and updated `check_code`
- `CHANGELOG.md` — Updated with latest automation changes

---

## 2026-04-22 — Enhance UI components with Alpine.js reactivity

**Summary**: Refactored core frontend components to improve versatility and user experience. The button component now supports automated loading states via Alpine.js, preventing double submissions and providing immediate visual feedback. Improved class inheritance and accessibility across UI atoms.

**Files Affected**:
- `templates/components/ui/button.html` — Refactored with Alpine.js `x-data` and DaisyUI spinners
- `CHANGELOG.md` — Updated with component evolution details

---

## 2026-04-24 — Frontend Standardization & Rebranding (Phase 1)

**Summary**: Standardized the frontend architecture and visual system. Centralized tokens using Tailwind v4 and DaisyUI v5 (Purple Fortress theme) with native Dark Mode support. Refactored UI components into an atomic system integrated with Alpine.js and HTMX 2.0. Improved form rendering reliability with django-widget-tweaks and corrected project-wide path resolution for template discovery.

**Files Affected**:
- `src/templates/base.html` — Modernized with global Alpine.js app state, HTMX listeners, and centralized CSS tokens
- `src/templates/components/navbar.html` — Updated with reactive theme toggle and standardized layout
- `src/templates/components/ui/input.html` — Standardized form input atom with widget-tweaks and robust error handling
- `src/templates/components/ui/button.html` — Enhanced with HTMX loading indicators and group-based states
- `src/templates/components/alert.html` — Refactored for Alpine.js lifecycle and DaisyUI semantics
- `src/templates/components/error_block.html` — Universal error handler for form and system messages
- `src/templates/account/login.html` & `signup.html` — Refactored to use new atomic UI system
- `src/config/settings/core/storage.py` & `database.py` — Corrected BASE_DIR for template discovery
- `src/requirements/base.txt` & `src/config/settings/base.py` — Integrated django-widget-tweaks
- `src/config/settings/third_party/allauth.py` — Updated LOGIN_REDIRECT_URL to dashboard
- `src/templates/landing/footer.html` & `cta.html` — UX and layout refinements

---

## Future Changes
