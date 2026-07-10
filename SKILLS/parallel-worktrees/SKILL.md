---
name: parallel-worktrees
description: >
  Workflow for managing parallel git worktrees to keep Engram context isolated per agent.
  Trigger: parallel work, git worktrees, Engram context issues.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Working on multiple branches concurrently with separate agents.
- Needing to keep agent memory context clean and isolated per branch.
- Avoiding destructive `git checkout` switches in a shared directory.

## Critical Patterns

- **Isolation**: One agent = One worktree = One branch.
- **Root Context**: Worktrees must reside *under* the project root directory so Engram persistent memory finds the expected context.
- **Git Hygiene**: `.gitignore` MUST include the worktree container directory (e.g., `worktree/`).
- **No Manual Switches**: Never try to make multiple agents work on the same folder using `git checkout`.

## Commands

```bash
# 1. Prepare container (run in project root)
mkdir -p worktree

# 2. Add worktrees
git worktree add ./worktree/<worktree-name> <branch-name>

# 3. Clean up
git worktree remove ./worktree/<worktree-name>
```

