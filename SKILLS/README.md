# SKILLS Index

Project-local reusable skills for Django Fortress SaaS development.

## Overview

All skills are located in `SKILLS/` and follow the [agentskills.io specification](https://agentskills.io/specification).

Each skill folder contains a `SKILL.md` definition. A skill may also include `references/` or `assets/` when they add useful supporting material.

---

## Available Skills

### Frontend Skills

#### django-htmx
**Path**: `SKILLS/django-htmx/SKILL.md`
**Version**: 1.0
**Author**: gentleman-programming

Django + HTMX + Alpine.js patterns for modern SaaS applications.

**Trigger**: When working with Django templates, HTMX requests, or HTMX+Alpine.js interactivity.

**When to Use**:
- Creating Django views that return HTMX responses
- Building reusable components with partial templates
- Adding reactivity with Alpine.js alongside HTMX
- Working with Django forms and HTMX form handling
- Implementing Django-allauth templates

**Assets**: `component_template.html` example

---

#### htmx-patterns
**Path**: `SKILLS/htmx-patterns/SKILL.md`
**Version**: 1.0
**Author**: gentleman-programming

HTMX advanced patterns: swap modifiers, events, OOB updates, indicators.

**Trigger**: When working with HTMX swap, events, loading states, or complex HTMX interactions.

**When to Use**:
- Implementing HTMX swap modifiers (innerHTML, beforeend, etc.)
- Using HTMX events for lifecycle management
- Out-of-band (OOB) updates
- Loading indicators and UX
- Boosted navigation
- SSE (Server-Sent Events) with HTMX
- WebSocket integration

---

### Authentication Skills

#### django-allauth
**Path**: `SKILLS/django-allauth/SKILL.md`
**Version**: 1.0
**Author**: gentleman-programming

Django allauth setup, configuration, and template patterns.

**Trigger**: When working with django-allauth, authentication, OAuth, or user account management.

**When to Use**:
- Setting up user authentication with django-allauth
- Configuring OAuth providers (Google, GitHub, etc.)
- Customizing allauth templates
- Working with email verification and password management
- Implementing social login

---

### Workflow Skills

#### parallel-worktrees
**Path**: `SKILLS/parallel-worktrees/SKILL.md`
**Version**: 1.1

**Trigger**: Feature or parallel Git worktrees, docs submodules, or branch isolation. Covers the root worktree plus the separate docs-submodule worktree and gitlink lifecycle.

#### local-work-unit-commits
**Path**: `SKILLS/local-work-unit-commits/SKILL.md`
**Version**: 1.0

**Trigger**: Multi-step implementation, commit planning, or any Git commit request. Defines task-scoped staging, pre-commit checks, and explicit approval before every individual commit.

#### template-repo-workflow
**Path**: `SKILLS/template-repo-workflow/SKILL.md`
**Version**: 1.1

**Trigger**: Initializing or syncing downstream SaaS projects, collaborative/extensible mode, or contributing changes to the upstream template.

### Project Architecture Skills

#### local-architecture-docs
**Path**: `SKILLS/local-architecture-docs/SKILL.md`
**Version**: 2.1

**Trigger**: Editing documentation, ADRs, indexes, or governance rules. Covers the `docs/` Git submodule, its independent worktree/branch, and parent gitlink.

#### local-architecture-routing
**Path**: `SKILLS/local-architecture-routing/SKILL.md`
**Version**: 1.0

**Trigger**: Creating or modifying Django URL patterns, app routes, HTMX endpoints, or API versioning.

#### local-architecture-templates
**Path**: `SKILLS/local-architecture-templates/SKILL.md`
**Version**: 2.2

**Trigger**: Modifying Django templates, components, rendering, or styling conventions.

---

## How Skills Are Loaded

### For Agents

1. **Discovery**: Agent reads `.atl/skill-registry.md` to find available skills
2. **Decision**: Agent decides which skills to activate based on task trigger
3. **Load**: Agent reads full SKILL.md from project-local path (`SKILLS/*/SKILL.md`)
4. **Execute**: Agent applies patterns and conventions from the skill

### For Orchestrators (SDD Phases)

1. **Compact Rules Injection**: Orchestrator resolves skill triggers, loads matching SKILLS
2. **Sub-Agent Prompt**: Orchestrator injects relevant skill content into sub-agent prompt as `## Project Standards (auto-resolved)`
3. **Progressive Disclosure**: Full skill rules provided at execution time, not pre-loaded

---

## Extending Skills

To add a new project-local skill:

1. Create folder: `SKILLS/{skill-name}/`
2. Create `SKILL.md` with YAML frontmatter following [agentskills.io spec](https://agentskills.io/specification)
3. Add to `.atl/skill-registry.md` table
4. Optionally add `references/` and `assets/` folders
5. Update this index with skill description

---

## Reference

- **Spec**: https://agentskills.io/specification
- **Agent Config**: `AGENTS.md`
- **Registry**: `.atl/skill-registry.md`
- **Changelog**: `CHANGELOG.md`
