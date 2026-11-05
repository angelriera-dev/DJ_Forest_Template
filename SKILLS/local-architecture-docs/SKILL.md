---
name: local-architecture-docs
description: >
  Use this skill when editing files in docs/ or updating ADRs, governance docs,
  change summaries, documentation indexes, or documentation conventions for this
  repository. It describes the local architecture and operating rules specific
  to the docs/ area of this project.
license: MIT
metadata:
  author: rag
  version: "2.1"
---

## When to Use

Use this skill when:

- Editing documentation in `docs/`
- Creating or updating ADRs in `docs/adr/`
- Updating documentation indexes or navigation
- Documenting workflow, migration, or integration changes
- Revising folder-scoped documentation conventions for this repository

If the task changes project-wide workflow, architecture, or integration rules, follow `docs/workflow-governance.md` before implementation.

## Local Scope

- Primary folder: `docs/`
- Key decision records: `docs/adr/`
- Governance process: `docs/workflow-governance.md`

## Git Submodule Rules

The project-root `docs/` directory is a separate Git wiki submodule. Read `docs/SKILL.md` and `docs/workflow-governance.md` for its full lifecycle.

- Check `git submodule status docs`; do not edit an uninitialized path.
- In a task worktree, keep a separate docs worktree/branch at the exact root gitlink. Verify the docs `HEAD` matches `git rev-parse :docs` before editing.
- Commit wiki content in its own repository and feature branch. The root repository records that commit later as the `docs` gitlink; these are distinct commits and require separate user approval.
- The root repository's Git hooks do not automatically run inside the docs submodule. Review and obtain approval for each docs commit separately.
- If publishing is later authorized, publish the wiki commit before the parent commit that references it.

## Core Rules

1. Keep documentation concise and canonical.
2. Link to files instead of duplicating large content blocks.
3. Put governance process details in `docs/workflow-governance.md`, not in multiple files.
4. Record verified user-facing changes in the parent repository's `CHANGELOG.md` before the corresponding commit.
5. Keep documentation in English.

## Default Procedure

1. Classify the change as local-only or governance-impacting and verify the docs submodule/worktree state.
2. For governance changes, update the ADR and process context before source implementation.
3. After implementation and verification, update the affected user-facing docs and parent `CHANGELOG.md` before their commit.
4. Validate referenced paths and commands in the correct repository context.
5. Show the exact staged diff and obtain explicit approval before each commit; never infer permission to publish.

## Reference

- `AGENTS.md`
- `docs/workflow-governance.md`
- `docs/adr/`
- `CHANGELOG.md`
