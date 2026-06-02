
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
	$(UV_CMD) run src/manage.py runserver --settings=config.settings.dev

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

check:
	$(UV_CMD) run src/manage.py check

pytest:
	$(UV_CMD) run pytest --cov=$(SRC_DIR)/apps --cov-report=term-missing

lint:
	$(UV_CMD) run ruff check $(SRC_DIR)

check_types:
	$(UV_CMD) run pyright $(SRC_DIR)

security_scan:
	@echo "Running Bandit (Security Linter)..."
	$(UV_CMD) run bandit -r $(SRC_DIR)/apps/ $(SRC_DIR)/config/ --ini .bandit
	@echo "Running Semgrep (OWASP Scans)..."
	$(UV_CMD) run semgrep scan --config auto $(SRC_DIR)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache .temp_venv .coverage uv.lock

run_tests: clean check lint check_types security_scan pytest



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

TEMPLATE_URL := https://github.com/angelriera-dev/Sass_Forest_Bolier.git

saas-init:
	@echo "Configuring upstream template for Extensible mode..."
	git remote add template $(TEMPLATE_URL) || echo "Remote 'template' already exists."
	@echo "Done. Use 'make saas-sync' to pull updates."

saas-sync:
	@echo "create a new branch"
	@git checkout -b update-template
	@echo "Fetching updates from template..."
	git fetch template
	@echo "Merging updates..."
	git merge template/main --allow-unrelated-histories
