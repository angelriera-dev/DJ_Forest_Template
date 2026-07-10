
# Configuración de UV
UV_CMD := $(shell which uv 2>/dev/null)
ifeq ($(UV_CMD),)
    @echo "UV not found. Please install it: pip install uv"
endif


SRC_DIR := src



# ===================================================================
# =========================== ENVIRONMENT ===========================
# ===================================================================

init:
	uv sync

dev:
	$(UV_CMD) run src/manage.py runserver --settings=config.settings.dev 0.0.0.0:8000

staging:
	$(UV_CMD) run src/manage.py runserver --settings=config.settings.staging

prod:
	$(UV_CMD) run src/manage.py runserver --settings=config.settings.prod



clear_migrations:
	@echo "warning - are you sure you want to remove all migrations? [y/n]"
	read -r answer
	if [ "$$answer" = "y" ]; then rm -rf **/migrations/*; fi

makemigrations:
	$(UV_CMD) run src/manage.py makemigrations


migrate:
	$(UV_CMD) run src/manage.py migrate



# ===================================================================
# ========================= QUALITY TEST ============================
# ===================================================================

check_code autotype:
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

pytest:
	$(UV_CMD) run pytest --cov=$(SRC_DIR)/apps --cov-report=term-missing

cs:
	@echo "Running Bandit (Security Linter)..."
	$(UV_CMD) run bandit -r $(SRC_DIR)/apps/ $(SRC_DIR)/config/ --ini .bandit
	@echo "Running Semgrep (OWASP Scans)..."
	$(UV_CMD) run semgrep scan --config auto $(SRC_DIR)

test: cs pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 
	rm -rf .pytest_cache .ruff_cache .temp_venv .coverage **/*.sqlite3


# ===============================================================
# ========================== DOCKER =============================
# ===============================================================

APP_NAME := app

dev_container:
	@docker compose up -d --build
	@docker compose exec $(APP_NAME) bash
	# @bash -lc '\
	# if docker ps --filter "name=app-app" --format "{{.Names}}" | grep -q "app-app"; then \
	# 	echo "Development container already running."; \
	# else \
	# 	echo "Starting development containers..."; \
	# 	docker compose -f docker-compose.yml --project-name $(APP_NAME) up -d --build; \
	# 	sleep 2; \
	# fi; \
	# exec docker compose -f docker-compose.yml --project-name $(APP_NAME) exec $(APP_NAME) bash'

clear_container:
	@docker compose down

rm-containers:
	@ids="$(shell docker ps -aq)"; \
	if [ -n "$$ids" ]; then docker stop $$ids && docker rm $$ids; else echo "no containers"; fi


temp:
	@docker run -it --rm -v .:/app -w /app  python:slim /bin/bash -c "adduser --disabled-password --gecos '' --uid 1000 devuser && su devuser"



# ===================================================================
# ===================== TEMPLATE REPOSITORY WORKFLOW =================
# ===================================================================

TEMPLATE_URL := https://github.com/angelriera-dev/Saas_Forest_Bolier.git

template-init:
	@echo "Configuring upstream template for Extensible mode..."
	git remote add template $(TEMPLATE_URL) || echo "Remote 'template' already exists."
	@echo "Done. Use 'make saas-sync' to pull updates."

template-sync:
	@git checkout -b update-template
	@git fetch template
	@git merge --squash --allow-unrelated-histories template/main

# Reverse workflow: contribute clean commits back to template (PR to template/main).
# Branch starts from template/main, so the PR shows only your chosen diff, not origin history.
TEMPLATE_BRANCH ?= main
TEMPLATE_CONTRIB_BRANCH ?= contribute-to-template

template-contribute:
	git fetch template
	git checkout -b $(TEMPLATE_CONTRIB_BRANCH) template/$(TEMPLATE_BRANCH)
	@echo "Rama '$(TEMPLATE_CONTRIB_BRANCH)' creada desde template/$(TEMPLATE_BRANCH)."
	@echo "Trae SOLO los archivos que quieras aportar (desde tu rama/commit actual):"
	@echo "  git checkout <tu-rama> -- ruta/archivo        # archivo completo"
	@echo "  git restore --source=<tu-rama> --patch -- ruta/archivo   # hunks selectivos"
	@echo "  git add ruta/archivo && git commit -m 'feat: ...'   # commit controlado"
	@echo "Repite para cada cambio. Luego abre el PR:"
	@echo "  git push template $(TEMPLATE_CONTRIB_BRANCH)"
	@echo "  gh pr create --repo angelriera-dev/Saas_Forest_Bolier --base $(TEMPLATE_BRANCH) --head $(TEMPLATE_CONTRIB_BRANCH)"

# Push the contribution branch to the template remote.
template-contribute-push:
	git push template $(TEMPLATE_CONTRIB_BRANCH)

# Integrity gate: abort if the diff vs template/main has forbidden/project-private files.
template-pr-check:
	SKILLS/local-architecture-templates/scripts/template-pr-check.sh
