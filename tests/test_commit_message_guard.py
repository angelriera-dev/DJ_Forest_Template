from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "commit_message_guard.py"


def run_git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)  # noqa: S603, S607


def run_guard(repo: Path, message_file: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603
        [sys.executable, str(SCRIPT), str(message_file)],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )


def create_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    run_git(repo, "init", "--quiet")
    run_git(repo, "checkout", "-b", "feature/guarded")
    (repo / "AGENTS.md").write_text("# Test project\n", encoding="utf-8")
    task_dir = repo / "odd" / "tasks"
    task_dir.mkdir(parents=True)
    (task_dir / "guarded.md").write_text(
        "# Feature\n\n## Tasks\n\n"
        "- T3 [S1-S2] — status: in_progress; task; route: inline; "
        "paths: `allowed.py`; commit: pending.\n\n## Log\n",
        encoding="utf-8",
    )
    return repo


def test_accepts_one_matching_trailer_without_changing_message(tmp_path: Path) -> None:
    repo = create_repo(tmp_path)
    message = repo / "COMMIT_EDITMSG"
    original = "feat: implement guard\n\nWork-Unit: guarded/T3\n"
    message.write_text(original, encoding="utf-8")

    result = run_guard(repo, message)

    assert result.returncode == 0
    assert result.stdout == "Commit message guard passed: Work-Unit: guarded/T3.\n"
    assert result.stderr == ""
    assert message.read_text(encoding="utf-8") == original


def test_rejects_missing_or_duplicate_or_mismatched_trailer_without_changing_message(
    tmp_path: Path,
) -> None:
    repo = create_repo(tmp_path)
    cases = (
        "feat: no trailer\n",
        "feat: body mention\n\nWork-Unit: guarded/T3\n\nMore body text\n",
        "feat: duplicate\n\nWork-Unit: guarded/T3\nWork-Unit: guarded/T3\n",
        "feat: wrong task\n\nWork-Unit: guarded/T2\n",
    )
    for original in cases:
        message = repo / "COMMIT_EDITMSG"
        message.write_text(original, encoding="utf-8")

        result = run_guard(repo, message)

        assert result.returncode == 1
        assert result.stdout == ""
        assert result.stderr == (
            "Commit message rejected: commit message must contain exactly one "
            "'Work-Unit: guarded/T3' trailer.\n"
        )
        assert message.read_text(encoding="utf-8") == original
