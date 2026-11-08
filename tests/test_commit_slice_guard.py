from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "commit_slice_guard.py"


def run_git(repo: Path, *args: str) -> str:
    # Test commands use fixed Git arguments in an isolated temporary repo.
    result = subprocess.run(  # noqa: S603
        ["git", *args],  # noqa: S607
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def create_repo(tmp_path: Path, *, task_lines: str | None = None) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    run_git(repo, "init", "--quiet")
    run_git(repo, "checkout", "-b", "feature/guarded")
    (repo / "AGENTS.md").write_text("# Test project\n", encoding="utf-8")
    task_dir = repo / "odd" / "tasks"
    task_dir.mkdir(parents=True)
    if task_lines is None:
        task_lines = (
            "- T1 [S1] — status: in_progress; task; route: inline; "
            "paths: `allowed.py`; commit: pending.\n"
        )
    task_doc = f"# Feature\n\n## Tasks\n\n{task_lines}\n## Log\n"
    (task_dir / "guarded.md").write_text(task_doc, encoding="utf-8")
    return repo


def stage(repo: Path, name: str, content: str) -> None:
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    run_git(repo, "add", name)


def run_guard(repo: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603
        [sys.executable, str(SCRIPT)],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )


def staged_paths(repo: Path) -> list[str]:
    return run_git(repo, "diff", "--cached", "--name-only").splitlines()


def test_allows_staged_paths_within_the_active_task(tmp_path: Path) -> None:
    repo = create_repo(tmp_path)
    stage(repo, "allowed.py", "value = 1\n")

    result = run_guard(repo)

    assert result.returncode == 0
    assert result.stdout == (
        "Commit slice guard passed: T1; staged files=1; changed lines=1.\n"
    )
    assert result.stderr == ""
    assert staged_paths(repo) == ["allowed.py"]


def test_allows_staged_paths_matching_a_declared_glob(tmp_path: Path) -> None:
    tasks = (
        "- T1 [S1] — status: in_progress; task; route: inline; "
        "paths: `src/*.py`; commit: pending.\n"
    )
    repo = create_repo(tmp_path, task_lines=tasks)
    stage(repo, "src/allowed.py", "value = 1\n")

    result = run_guard(repo)

    assert result.returncode == 0
    assert result.stdout == (
        "Commit slice guard passed: T1; staged files=1; changed lines=1.\n"
    )
    assert result.stderr == ""
    assert staged_paths(repo) == ["src/allowed.py"]


def test_rejects_paths_outside_the_active_task_without_changing_the_index(
    tmp_path: Path,
) -> None:
    repo = create_repo(tmp_path)
    stage(repo, "allowed.py", "value = 1\n")
    stage(repo, "outside.py", "value = 2\n")
    before = staged_paths(repo)

    result = run_guard(repo)

    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr == (
        "Commit slice rejected: staged path(s) outside T1 scope: outside.py\n"
    )
    assert staged_paths(repo) == before


def test_rejects_more_than_400_changed_lines_without_changing_the_index(
    tmp_path: Path,
) -> None:
    repo = create_repo(tmp_path)
    stage(repo, "allowed.py", "".join(f"value_{i} = {i}\n" for i in range(401)))
    before = staged_paths(repo)

    result = run_guard(repo)

    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr == (
        "Commit slice rejected: 401 changed lines exceeds the 400-line limit.\n"
    )
    assert staged_paths(repo) == before


def test_rejects_multiple_active_tasks_without_changing_the_index(
    tmp_path: Path,
) -> None:
    tasks = (
        "- T1 [S1] — status: in_progress; first; route: inline; "
        "paths: `allowed.py`; commit: pending.\n"
        "- T2 [S1] — status: in_progress; second; route: inline; "
        "paths: `other.py`; commit: pending.\n"
    )
    repo = create_repo(tmp_path, task_lines=tasks)
    stage(repo, "allowed.py", "value = 1\n")
    before = staged_paths(repo)

    result = run_guard(repo)

    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr == (
        "Commit slice rejected: task manifest must contain exactly one "
        "in-progress task; found 2.\n"
    )
    assert staged_paths(repo) == before


def test_rejects_unsafe_task_paths_without_changing_the_index(
    tmp_path: Path,
) -> None:
    tasks = (
        "- T1 [S1] — status: in_progress; task; route: inline; "
        "paths: `../outside.py`; commit: pending.\n"
    )
    repo = create_repo(tmp_path, task_lines=tasks)
    stage(repo, "allowed.py", "value = 1\n")
    before = staged_paths(repo)

    result = run_guard(repo)

    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr == (
        "Commit slice rejected: task T1 has an unsafe path: ../outside.py.\n"
    )
    assert staged_paths(repo) == before


def test_keeps_existing_precommit_hooks_and_registers_slice_guard() -> None:
    config = Path(__file__).resolve().parents[1] / ".pre-commit-config.yaml"
    text = config.read_text(encoding="utf-8")

    assert "id: trailing-whitespace" in text
    assert "id: ruff" in text
    assert "id: ruff-format" in text
    assert "id: commit-slice-guard" in text
    assert "id: commit-message-guard" in text
    assert "stages: [commit-msg]" in text


def test_make_target_installs_pre_commit_hook() -> None:
    makefile = Path(__file__).resolve().parents[1] / "Makefile"
    text = makefile.read_text(encoding="utf-8")

    assert "git-hooks:" in text
    assert "pre-commit install --hook-type pre-commit" in text
    assert "pre-commit install --hook-type commit-msg" in text
