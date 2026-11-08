---
name: local-work-unit-commits
description: >
  Plan and validate project-local commits as one verified work unit at a time.
  Trigger: multi-step implementation, commit planning, or any Git commit request.
license: MIT
metadata:
  author: rag
  version: "1.0"
  chat_decisions_checked: "YES"
---

## When to Use

Use this skill when implementing tracked work, preparing a commit, or deciding what belongs in a commit.

## Rules

1. **Get approval for each commit.** Implementation authorization is not commit authorization. Before every `git commit`, show the staged paths, diff summary, and exact message, then wait for approval of that one commit. A prior commit approval does not carry over. Pushes and pull requests need separate authorization.
2. **One task per commit.** Keep tests and documentation for that behavior with the behavior. Split by independently reviewable task, not by file type; target no more than 400 changed diff lines (additions plus deletions) per commit.
3. **Declare the scope.** For tracked feature work, name the branch `feature/<slug>` and the task file `odd/tasks/<slug>.md`. Each task line declares `status`, backticked `paths` globs, and commit evidence. Keep exactly one task `in_progress` and stage only files matching its paths; the task document itself is explicitly listed when it changes.
4. **Use the guard.** Run `make git-hooks` once per clone. The pre-commit hook enforces the active task's allowed paths and the 400-line limit; the commit-msg hook requires exactly one matching `Work-Unit: <slug>/<task-id>` trailer. Do not bypass a failed hook with `--no-verify`; fix the scope or ask the user to revise it.
5. **Review the final staged state.** Run relevant checks before asking. If a hook changes the index or working tree, restage and request approval again for the changed diff.
6. **Keep the documentation repository distinct.** `docs/` is a Git submodule. Its content commit and the parent repository's gitlink commit are separate work units and need separate approval. The root hooks do not install themselves in the docs repository.

The hooks are local safeguards, not proof of human consent. They may be bypassed; the explicit approval step remains mandatory. Small, untracked ODD work still requires per-commit approval and remains subject to the 400-line hook limit.

## References

- `docs/workflow-governance.md`
- `docs/SKILL.md`
- `SKILLS/parallel-worktrees/SKILL.md`
- `AGENTS.md`
