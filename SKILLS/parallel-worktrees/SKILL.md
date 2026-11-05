---
name: parallel-worktrees
description: >
  Workflow for managing feature and parallel git worktrees, including a nested docs-submodule worktree.
  Trigger: feature worktrees, parallel work, docs submodules, or Engram context issues.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.1"
---

## When to Use

- Working on multiple branches concurrently with separate agents.
- Needing to keep agent memory context clean and isolated per branch.
- Avoiding destructive `git checkout` switches in a shared directory.
- Editing project documentation stored in a Git submodule.

## Critical Patterns

- **Isolation**: One agent = One worktree = One branch.
- **Root Context**: Worktrees must reside *under* the project root directory (e.g. `./worktree/<worktree-name>`) so Engram persistent memory finds the expected context.
- **Git Hygiene**: `.gitignore` MUST include the worktree container directory (e.g., `worktree/`).
- **No Manual Switches**: Never try to make multiple agents work on the same folder using `git checkout`.
- **Sub-Agent Constraint**: Sub-agents MUST NOT invoke git worktree commands. They inherit the locked workspace and must execute all operations strictly inside their designated `workdir`.
- **Orchestrator Enforcement**: The root orchestrator is sole responsible for creating and cleaning worktrees, and launching sub-agents with `workdir` pointed to the worktree path.
- **Preserve work**: Never remove a worktree with uncommitted changes. Do not use `--force`; preserve branches unless cleanup is explicitly safe and authorized.

## Docs Submodule Worktrees

The project-root `docs/` directory is a separate Git repository. A new parent worktree may leave it uninitialized; do not edit the empty path.

1. Inspect `git submodule status docs` and record the root gitlink with `git -C <root-worktree> rev-parse :docs`.
2. Use an independent docs worktree/feature branch at that exact commit. Keep one docs branch per task; never switch or commit on the wiki default branch.
3. Verify the docs worktree `HEAD` equals the root gitlink before editing. After the wiki commit, update the parent `docs` gitlink deliberately; the two commits have separate histories and require separate approval.
4. A parent repository hook is not installed in the submodule automatically. Review each wiki commit separately. If publishing is authorized, make the referenced wiki commit available remotely before publishing the parent gitlink.
5. See `SKILLS/local-architecture-docs/SKILL.md` and `docs/SKILL.md` for the detailed docs workflow.

## Commands

```bash
# 1. Prepare container (run in project root)
mkdir -p worktree

# 2. Add a root worktree from the selected base
git worktree add -b feature/<task> ./worktree/<task> <base-ref>

# 3. After verifying it is clean, remove only when cleanup is authorized
git worktree remove ./worktree/<worktree-name>
```

