# Configuración de UV
UV_CMD := $(shell which uv 2>/dev/null)
ifeq ($(UV_CMD),)
    @echo "UV not found. Please install it: pip install uv"
endif


SRC_DIR := src

# ===================================================================
# =============================== HELP ==============================
# ===================================================================

help: ## Show this help
	@echo "Available targets:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "For targets without a '##' description, read the Makefile directly."

# ===================================================================
# =========================== ENVIRONMENT ===========================
# ===================================================================

init: ## Sync dependencies with UV
	uv sync

dev: ## Run dev server (port 8000)
	$(UV_CMD) run src/manage.py runserver --settings=config.settings.dev 0.0.0.0:8000

staging: ## Run staging server
	$(UV_CMD) run src/manage.py runserver --settings=config.settings.staging

prod: ## Run prod server
	$(UV_CMD) run src/manage.py runserver --settings=config.settings.prod


clear_migrations: ## Remove ALL migrations (destructive, interactive)
	@echo "warning - are you sure you want to remove all migrations? [y/n]"
	read -r answer
	if [ "$$answer" = "y" ]; then rm -rf **/migrations/*; fi

makemigrations: ## Generate migrations
	$(UV_CMD) run src/manage.py makemigrations


migrate: ## Apply migrations
	$(UV_CMD) run src/manage.py migrate


# ===================================================================
# ========================= QUALITY TEST ============================
# ===================================================================

install-git-hooks: ## Install the configured repository pre-commit hook
	$(UV_CMD) run pre-commit install --hook-type pre-commit

check_code autotype: ## Lint, format, autotype and type-check
	$(UV_CMD) run ruff check --fix
	$(UV_CMD) run ruff format --check $(SRC_DIR)
	$(UV_CMD) run righttyper \
		--output-files \
		--overwrite \
		--include-files '^(?!.*(migrations|tests|settings|wsgi|asgi|manage)).*\.py$$' \
		-m pytest $(SRC_DIR) --continue-on-collection-errors
	$(UV_CMD) run autotyping $(SRC_DIR) --none-return --scalar-return --bool-param --guess-common-names
	$(UV_CMD) run ruff format $(SRC_DIR)
	$(UV_CMD) run pyright $(SRC_DIR)

	@echo "✅ Autotipado completo. Revisa con: git diff"

pytest: ## Run tests with coverage
	$(UV_CMD) run pytest --cov=$(SRC_DIR)/apps --cov-report=term-missing

cs: ## Run Bandit + Semgrep security scans
	@echo "Running Bandit (Security Linter)..."
	$(UV_CMD) run bandit -r $(SRC_DIR)/apps/ $(SRC_DIR)/config/ --ini .bandit
	@echo "Running Semgrep (OWASP Scans)..."
	$(UV_CMD) run semgrep scan --config auto $(SRC_DIR)

test: cs pytest ## Run security scans + tests

clean: ## Remove caches, coverage data and sqlite files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache .temp_venv .coverage **/*.sqlite3


# ===============================================================
# ========================== DOCKER =============================
# ===============================================================

APP_NAME := app

dev_container: ## Start Docker dev containers and exec into app
	@docker compose up -d --build
	@docker compose exec $(APP_NAME) bash

clear_container: ## Stop and remove Docker dev containers
	@docker compose down

rm-containers:
	@ids="$(shell docker ps -aq)"; \
	if [ -n "$$ids" ]; then docker stop $$ids && docker rm $$ids; else echo "no containers"; fi


temp:
	@docker run -it --rm -v .:/app -w /app  python:slim /bin/bash -c "adduser --disabled-password --gecos '' --uid 1000 devuser && su devuser"



# ===================================================================
# ===================== TEMPLATE REPOSITORY WORKFLOW =================
# ===================================================================

TEMPLATE_URL := https://github.com/angelriera-dev/DJ_Forest_Template.git
TEMPLATE_REPO := angelriera-dev/DJ_Forest_Template

template-init: ## Register the upstream template remote
	@echo "Configuring upstream template for Extensible mode..."
	git remote add template $(TEMPLATE_URL) || echo "Remote 'template' already exists."
	@echo "Done. Use 'make template-sync' to pull updates."

template-sync: ## Pull template updates into a squash-merge branch
	@git checkout -b update-template
	@git fetch template
	@git merge --squash --allow-unrelated-histories template/main

# Reverse workflow: contribute clean commits back to template (PR to template/main).
# Branch starts from template/main, so the PR shows only your chosen diff, not origin history.
TEMPLATE_BRANCH ?= main
TEMPLATE_CONTRIB_BRANCH ?= contribute-to-template

template-contribute: ## Start contribution branch from template/main (guided)
	git fetch template
	git checkout -b $(TEMPLATE_CONTRIB_BRANCH) template/$(TEMPLATE_BRANCH)
	@echo "Rama '$(TEMPLATE_CONTRIB_BRANCH)' creada desde template/$(TEMPLATE_BRANCH)."
	@echo "Trae SOLO los archivos que quieras aportar (desde tu rama/commit actual):"
	@echo "  git checkout <tu-rama> -- ruta/archivo        # archivo completo"
	@echo "  git restore --source=<tu-rama> --patch -- ruta/archivo   # hunks selectivos"
	@echo "  git add ruta/archivo && git commit -m 'feat: ...'   # commit controlado"
	@echo "Repite para cada cambio. Luego abre el PR:"
	@echo "  git push template $(TEMPLATE_CONTRIB_BRANCH)"
	@echo "  gh pr create --repo $(TEMPLATE_REPO) --base $(TEMPLATE_BRANCH) --head $(TEMPLATE_CONTRIB_BRANCH)"

# Push the contribution branch to the template remote.
template-contribute-push: ## Push the contribution branch to the template remote
	git push template $(TEMPLATE_CONTRIB_BRANCH)

# Integrity gate: abort if the diff vs template/main has forbidden/project-private files.
template-pr-check: ## Abort if diff vs template/main contains forbidden files
	SKILLS/local-architecture-templates/scripts/template-pr-check.sh

# Show focused diff vs template/main (review helper).
template-diff: ## Show diff vs template/main
	SKILLS/local-architecture-templates/scripts/template-diff.sh
