# Docker Environment Configuration
Status: Implementation verified; native review blocked pending host model routing; delivery strategy: ask-on-risk. Scope is local dev/staging operation and portable production configuration, with no provider-specific deployment.

## Specs
1. **S1** — User request: “el foco principal es tener un proyecto de seguridad robusta para implementar en la nube pero manteniendo la simplicidad”; environment files may contain necessary code: “los archivos de configuracion @src/config/settings/dev.py y resto de entornos si pueden hacer el uso necesario de codigo”.
2. **S2** — Selected scope: “Perfil y ejecución local” for staging; no cloud deployment configuration. Staging may optionally point at a cloud database: “la url de stagin seria opcional agregar una url de la nube o usar un servicio local de postgres”.
3. **S3** — Selected local database model: “Un contenedor, bases separadas (Recomendado)”. Development SQLite data “Se pueden descartar”.
4. **S4** — Selected Make behavior: “Copiar si falta (Recomendado)”; never overwrite existing `.env`. The production URL is outside Make: “Make nunca la lee ni modifica (Recomendado)”.
5. **S5** — “Preparación portable (Recomendado)”: production app/image configuration may be supplied by a platform, without configuring a specific provider or deploying. Staging requires safe explicit configuration when using cloud: “Sí al usar cloud (Recomendado)”.
6. **S6** — No staging/prod mail integration is requested. Dev keeps console mail; production email can be implemented later.
7. **S7** — Keep the existing root `Dockerfile` as runtime image and `docker/dev.Dockerfile` for dev; use the runtime image for local staging and production. No separate staging/prod Dockerfiles.
8. **S8** — Local PostgreSQL data persists in a project-local bind mount; ordinary stop/cleanup must not delete it. Destructive reset must be explicit and environment-scoped.

## Tasks
- T1 — S1-S8 — inline — commit: wiki `c7b0976`; root `006fbe2` (governance context and implementation specification)
- T2 — S1,S2,S5 — inline — commit: `006fbe2` (environment-specific settings, runtime selection, and strict validation)
- T3 — S2-S4,S7,S8 — inline — commit: `0eeac9d` (local PostgreSQL roles/databases, Docker, and thin Make targets; repair the stale dev dependency path)
- T4 — S1-S8 — inline — commit: tests `006fbe2`; ADR/operator docs `c7b0976`; README/workflow integration `0eeac9d` (configuration tests and operator documentation)
- T5 — S1-S8 — inline — commit: verification for `006fbe2` and `0eeac9d`; native review blocked pending model routing (focused/full checks and final review)

## Log
- L1 — User’s original request: “en el make file existen scripts de docker la idea principal es poder levantar este proyecto en los 3 entornos, stagin, dev, prod, usando las variables correctas ( enviromen ), el archivo make debe generar las variables a partir del archivo @.env.example , ayudame primero a analizar correctamente como deberia funcionar cada entorno, cual seria el flujo de trabajo de cada entorno posibles variables y restricciones”
- L2 — Authorization: “autorizo la implementacion segun el plan”
- L3 — User clarified the security goal and minimal Make configuration: “el foco principal es tener un proyecto de seguridad robusta para implementar en la nube pero manteniendo la simplicidad, examina a fonda si puede seguir existiendo ambiguedad en los requerimientos y sientete libre de preguntarme otra vez.”
- L4 — User clarified Docker image layout: “perfecto esta aclarado todo, esta completamente claro el plan de implementacion”
- L5 — Chat decision check: YES; implementation scope and constraints were confirmed in chat before creating this specification.
- L6 — Repository evidence before implementation: `docker/dev.Dockerfile` copies nonexistent `src/requirements/`; `pyproject.toml`/`uv.lock` contained no PostgreSQL driver; production Gunicorn loads `config.wsgi`, but WSGI/ASGI defaulted to the empty `config.settings` package; PostgreSQL settings existed only for prod, and no staging module existed. These findings expand implementation only as necessary to make the agreed environments run.
- L7 — During verification, confirmed that `DATABASE_URL` may point to cloud PostgreSQL while the staging app itself still runs locally over HTTP. Separated web HTTPS policy from database URL detection; cloud staging enables HTTPS redirects only through explicit `DJANGO_SECURE_SSL_REDIRECT=true`.
- L8 — Final security review found that the runtime image would otherwise inherit the settings package's `dev` default if the platform omitted `DJANGO_ENV`. Set the runtime image default to `prod`; staging Compose explicitly overrides it. Verify the image fails closed with missing production variables.
- L9 — User selected “Crear rama de reemplazo” after the environment blocked a destructive reset. Rebuilt the implementation without pushing, preserving `feature/docker-environments` at `4218e0e`; replacement branch `feature/docker-environments-sliced` contains settings/runtime commit `006fbe2` and Docker/Make commit `0eeac9d`. The wiki docs commit is `c7b0976`.
- L10 — Final checks passed: 45 passed, 10 skipped; Ruff, Pyright, Bandit, Compose config, Docker builds, staging settings/HTTP smoke, persistence, and diff checks passed. Full Semgrep reported 13 findings in 7 unchanged paths; changed settings scan reported none. Independent verification found no blocker in T2/T3. Native assess marked the feature slice high risk/review due; host relay then failed before any reviewer ran because `review-risk` has no model configured. One fresh bound STATUS reoffered the full four-slot group, not the requested single slot, so no further capture or acknowledgement was submitted. Native review remains blocked until host model routing is configured; no push or native approval is claimed.
