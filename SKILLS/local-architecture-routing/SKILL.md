---
name: local-architecture-routing
description: >
  Trigger: routing, urls, url patterns, API routes, versioning, two-tier routing.
  Use this skill when creating or modifying Django URL patterns, adding new app routes,
  implementing API versioning, or refactoring routing structure. It describes the
  two-tier routing convention for this project.
license: MIT
metadata:
  author: rag
  version: "1.0"
---

## When to Use

Use this skill when:

- Adding new Django apps with URL patterns
- Creating API endpoints (HTMX partials or REST)
- Implementing API versioning (v1, v2, etc.)
- Refactoring existing routing structure
- Reviewing URL patterns for consistency

## Local Scope

- Standard views: `app/urls.py` + `app/views.py`
- API routes: `app/api/urls.py` + `app/api/views.py`
- Main URL config: `src/config/urls.py`
- ADR: `docs/adr/ADR-routing-convention.md`

## Core Rules

1. **Two-tier routing**: Separate standard views from API routes.
2. **Versioned API**: All REST endpoints use path-based versioning (`v1/`, `v2/`).
3. **Clear naming**: Use `<app>:<action>` for standard, `<app>:api_<resource>` for API.
4. **Underscores only**: No hyphens in URL names.
5. **API prefix**: REST endpoints return JSON, prefix names with `api_`.

## Decision Gates

| Route Type | Location | Mount Point | Response |
|------------|----------|-------------|----------|
| Full-page HTML | `app/urls.py` | `/<prefix>/` | HTML page |
| HTMX partial | `app/api/urls.py` | `/api/<app>/` | HTML fragment |
| REST endpoint | `app/api/urls.py` | `/api/<app>/v1/` | JSON |

## Default Procedure

1. **Classify the route**: Standard view, HTMX partial, or REST endpoint?
2. **Choose the file**: Standard → `app/urls.py`, API → `app/api/urls.py`
3. **Add version prefix**: REST endpoints go under `v1/` in `app/api/urls.py`
4. **Name the route**: Follow naming conventions (`<app>:<action>` or `<app>:api_<resource>`)
5. **Update main config**: Mount the app in `src/config/urls.py` if new app
6. **Test**: Verify route resolves correctly

## Adding a New App

```python
# src/config/urls.py
api_urlpatterns = [
    path("<app>/", include("apps.<app>.api.urls")),
]

urlpatterns = [
    # ... existing routes ...
    path("<prefix>/", include("apps.<app>.urls")),  # Standard views
    path("api/", include((api_urlpatterns, "api"))),  # API routes
]
```

## Adding REST Endpoint

```python
# app/api/urls.py
urlpatterns = [
    path("v1/<resource>/", views.<resource>_list, name="api_<resource>"),
]
```

## Reference

- `docs/adr/ADR-routing-convention.md` — Full ADR with examples
- `AGENTS.md` — Routing conventions section
- `src/config/urls.py` — Main URL configuration
