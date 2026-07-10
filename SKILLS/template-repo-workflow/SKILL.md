---
name: saas-workflow
description: >
  Use this skill to understand the workflow and constraints when a SaaS project
  is derived from this template, specifically the Extensible and Collaborative modes.
license: MIT
metadata:
  version: "1.0"
---

## When to Use

Use this skill when:
- Setting up a new SaaS repository from this template.
- Syncing upstream changes from the template to a SaaS project.
- Handling questions about what can or cannot be modified in a collaborative SaaS project.
- A user is confused about how to merge security updates from the template.

## The Two Workflows

This project supports two different workflows for downstream SaaS projects:

### 1. Extensible Mode (Authoritative)
- **Concept:** The downstream SaaS takes full ownership of the codebase.
- **Rules:** No files are blocked from editing. The developer can modify `config/`, `templates/`, or anything else.
- **Syncing:** They pull from upstream (`make saas-sync`) and manually resolve all conflicts.
- **Setup:** `make saas-init`

### 2. Collaborative Mode (Strict Protected)
- **Concept:** The downstream SaaS stays as close to the template as possible for core infrastructure, allowing easy unidirectional security updates.
- **Rules:**
  - `src/config/*`, `src/templates/components/*`, and `SKILLS/*` are STRICTLY BLOCKED from local modification via a git pre-commit hook.
  - `src/apps/users/*` triggers a WARNING but allows modification.
- **Syncing:** Updates are pulled cleanly via `make saas-sync` with minimal conflicts since protected files weren't touched.
- **Setup:** `make saas-collab`

## Agent Guidelines
- If an agent is working in a Collaborative SaaS project and tries to modify a protected file (like `config/settings.py`), it MUST stop and explain that the file is protected by the template. The change should be made in the upstream template repository instead, or the SaaS project must be converted to Extensible mode by removing the pre-commit hook.
- Do not create custom scripts for syncing; always use the `Makefile` commands (`saas-init`, `saas-collab`, `saas-sync`) or the raw bash one-liners documented in the `README.md`.
