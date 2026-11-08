#!/usr/bin/env python3
"""Reject staged changes that exceed or escape the active ODD work unit."""

from __future__ import annotations

import fnmatch
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

MAX_CHANGED_LINES = 400
TASK_LINE = re.compile(r"^\s*-\s+(T\d+)\s+\[[^]]+\]")
STATUS_FIELD = re.compile(r"\bstatus:\s*([^;]+);")
PATHS_FIELD = re.compile(r"\bpaths:\s*(.*?);\s*commit:")


class GuardError(ValueError):
    """A staged commit does not fit its declared work-unit boundary."""


@dataclass(frozen=True)
class Task:
    task_id: str
    status: str
    paths: tuple[str, ...]


def git_output(repo_root: Path, *args: str) -> bytes:
    # Internal callers pass fixed Git subcommands; no shell or user input is used.
    result = subprocess.run(  # noqa: S603
        ["git", *args],  # noqa: S607
        cwd=repo_root,
        check=True,
        capture_output=True,
    )
    return result.stdout


def staged_diff(repo_root: Path) -> tuple[list[str], int]:
    path_output = git_output(
        repo_root, "diff", "--cached", "--name-only", "--diff-filter=ACMRD", "-z"
    )
    paths = [os.fsdecode(path) for path in path_output.split(b"\0") if path]

    numstat = git_output(
        repo_root, "diff", "--cached", "--numstat", "--no-renames", "-z"
    )
    changed_lines = 0
    for record in numstat.split(b"\0"):
        if not record:
            continue
        fields = record.split(b"\t", 2)
        if len(fields) != 3:
            raise GuardError("could not parse the staged diff statistics.")
        added, deleted = fields[:2]
        if added != b"-" and deleted != b"-":
            changed_lines += int(added) + int(deleted)
    return paths, changed_lines


def project_root_for(repo_root: Path) -> Path:
    for candidate in (repo_root, *repo_root.parents):
        if (candidate / "AGENTS.md").is_file() and (candidate / ".git").exists():
            return candidate
    raise GuardError("could not locate the project root containing AGENTS.md.")


def task_manifest(project_root: Path, branch: str) -> Path | None:
    if not branch.startswith("feature/"):
        return None
    feature = branch.removeprefix("feature/")
    if not feature or "/" in feature:
        return None
    path = project_root / "odd" / "tasks" / f"{feature}.md"
    return path if path.is_file() else None


def parse_tasks(task_file: Path) -> list[Task]:
    in_tasks = False
    tasks: list[Task] = []
    for line in task_file.read_text(encoding="utf-8").splitlines():
        if line.strip() == "## Tasks":
            in_tasks = True
            continue
        if in_tasks and line.startswith("## "):
            break
        match = TASK_LINE.match(line) if in_tasks else None
        if not match:
            continue
        status = STATUS_FIELD.search(line)
        paths_field = PATHS_FIELD.search(line)
        if status is None or paths_field is None:
            raise GuardError(
                f"task {match.group(1)} must declare status and allowed paths."
            )
        paths = tuple(re.findall(r"`([^`]+)`", paths_field.group(1)))
        if not paths:
            raise GuardError(f"task {match.group(1)} has no allowed paths.")
        for path in paths:
            parts = Path(path).parts
            if Path(path).is_absolute() or ".." in parts:
                raise GuardError(f"task {match.group(1)} has an unsafe path: {path}.")
        tasks.append(Task(match.group(1), status.group(1).strip(), paths))
    return tasks


def active_task(project_root: Path, branch: str) -> tuple[str, Task] | None:
    manifest = task_manifest(project_root, branch)
    if manifest is None:
        return None
    tasks = parse_tasks(manifest)
    active = [task for task in tasks if task.status == "in_progress"]
    if len(active) != 1:
        raise GuardError(
            "task manifest must contain exactly one in-progress task; "
            f"found {len(active)}."
        )
    return branch.removeprefix("feature/"), active[0]


def validate_staged_changes(
    repo_root: Path,
    project_root: Path,
    paths: list[str],
    changed_lines: int,
    branch: str,
) -> str:
    if changed_lines > MAX_CHANGED_LINES:
        raise GuardError(
            f"{changed_lines} changed lines exceeds the {MAX_CHANGED_LINES}-line limit."
        )
    if not paths:
        return "Commit slice guard skipped: no staged paths."

    current = active_task(project_root, branch)
    if current is None:
        return (
            "Commit slice guard passed: no feature task manifest; "
            f"staged files={len(paths)}; changed lines={changed_lines}."
        )
    _, task = current
    prefix = repo_root.relative_to(project_root).as_posix()
    project_paths = [f"{prefix}/{path}" if prefix != "." else path for path in paths]
    out_of_scope = sorted(
        path
        for path in project_paths
        if not any(fnmatch.fnmatchcase(path, pattern) for pattern in task.paths)
    )
    if out_of_scope:
        raise GuardError(
            f"staged path(s) outside {task.task_id} scope: {', '.join(out_of_scope)}"
        )
    return (
        f"Commit slice guard passed: {task.task_id}; "
        f"staged files={len(paths)}; changed lines={changed_lines}."
    )


def main() -> int:
    try:
        # Fixed Git query; no user-controlled input reaches the command.
        repo_root = Path(
            subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"],  # noqa: S607
                text=True,
            ).strip()
        ).resolve()
        project_root = project_root_for(repo_root)
        branch = git_output(repo_root, "branch", "--show-current").decode().strip()
        paths, changed_lines = staged_diff(repo_root)
        message = validate_staged_changes(
            repo_root, project_root, paths, changed_lines, branch
        )
    except (GuardError, OSError, subprocess.CalledProcessError) as exc:
        detail = str(exc) or "Git command failed."
        print(f"Commit slice rejected: {detail}", file=sys.stderr)
        return 1

    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
