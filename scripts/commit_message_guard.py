#!/usr/bin/env python3
"""Require the active ODD task's Work-Unit commit-message trailer."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from commit_slice_guard import GuardError, active_task, project_root_for


def parse_trailers(message: str) -> list[str]:
    try:
        # Fixed Git parser; message text is passed on stdin, never as a command.
        result = subprocess.run(  # noqa: S603
            ["git", "interpret-trailers", "--parse"],  # noqa: S607
            input=message,
            text=True,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise GuardError("could not parse commit-message trailers.") from exc
    return result.stdout.splitlines()


def validate_message(message: str, expected: str | None) -> str:
    if expected is None:
        return "Commit message guard passed: no feature task manifest."
    work_units = [
        trailer
        for trailer in parse_trailers(message)
        if trailer.startswith("Work-Unit:")
    ]
    if work_units != [f"Work-Unit: {expected}"]:
        raise GuardError(
            f"commit message must contain exactly one 'Work-Unit: {expected}' trailer."
        )
    return f"Commit message guard passed: Work-Unit: {expected}."


def main() -> int:
    try:
        if len(sys.argv) != 2:
            raise GuardError("expected the commit-message file path.")
        repo_root = Path(
            subprocess.check_output(  # noqa: S603
                ["git", "rev-parse", "--show-toplevel"],  # noqa: S607
                text=True,
            ).strip()
        ).resolve()
        project_root = project_root_for(repo_root)
        branch = subprocess.check_output(  # noqa: S603
            ["git", "branch", "--show-current"],  # noqa: S607
            cwd=repo_root,
            text=True,
        ).strip()
        current = active_task(project_root, branch)
        expected = f"{current[0]}/{current[1].task_id}" if current else None
        message = Path(sys.argv[1]).read_text(encoding="utf-8")
        output = validate_message(message, expected)
    except (GuardError, OSError, subprocess.CalledProcessError) as exc:
        print(f"Commit message rejected: {exc}", file=sys.stderr)
        return 1
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
