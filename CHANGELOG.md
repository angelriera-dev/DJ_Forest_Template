# Changelog

## 2026-11-05 - Agent workflow and commit governance
- Documented isolated feature/docs worktrees and task-scoped commits with staged-path and 400-line guards.
- Added a matching `Work-Unit` commit-message trailer check and explicit approval before each commit.
- Aligned workflow guidance and skill indexes; recorded the existing documentation-submodule commit and its root gitlink process.

## 2026-06-12 - Consolidation and Refactoring of `src/apps/<app_name>/`
- Centralized context-building and session management into a new `SessionService` in `src/apps/<app_name>/services.py`.
- Refactored `views.py` and `api/views.py` to utilize `SessionService` for session state and <app_name> context, reducing code redundancy.
- Cleaned up `helpers.py` by removing deprecated session/context helper functions.
- Refactored the entire `src/apps/<app_name>/tests/` suite to align with the new service-based architecture, ensuring 100% pass rate in the <app_name> app test suite.
- Fixed critical bugs in phase-awareness and deferred persistence of SRS metrics uncovered during refactoring.
