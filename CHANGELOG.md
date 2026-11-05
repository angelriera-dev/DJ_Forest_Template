# Changelog

## 2026-11-05 - Local and Deployment Environment Configuration
- Added isolated dev/staging PostgreSQL databases, environment-aware Django settings, and a portable runtime image that defaults to production and fails closed when configuration is missing.
- Added safe local `.env` initialization, persistent project-local database storage, and operator guidance; no cloud deployment or email integration.

## 2026-06-12 - Consolidation and Refactoring of `src/apps/<app_name>/`
- Centralized context-building and session management into a new `SessionService` in `src/apps/<app_name>/services.py`.
- Refactored `views.py` and `api/views.py` to utilize `SessionService` for session state and <app_name> context, reducing code redundancy.
- Cleaned up `helpers.py` by removing deprecated session/context helper functions.
- Refactored the entire `src/apps/<app_name>/tests/` suite to align with the new service-based architecture, ensuring 100% pass rate in the <app_name> app test suite.
- Fixed critical bugs in phase-awareness and deferred persistence of SRS metrics uncovered during refactoring.
