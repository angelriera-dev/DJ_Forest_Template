
# Configuración de UV
UV := $(shell which uv 2>/dev/null)
VENV := .venv
PYTHON := $(VENV)/bin/python
SRC_DIR := src

# Si UV no está instalado, intentamos usarlo vía pip (fallback)
ifeq ($(UV),)
    UV_CMD := $(PYTHON) -m uv
else
    UV_CMD := uv
endif

install: init

init:
	@echo "Initializing environment with uv..."
	@if [ -z "$(UV)" ] && [ ! -f $(PYTHON) ]; then \
		python3 -m venv $(VENV) && \
		$(VENV)/bin/pip install uv; \
	fi
	$(UV_CMD) sync
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env from .env.example"; \
	fi

run: dev

dev:
	$(UV_CMD) run src/manage.py runserver

migrate:
	$(UV_CMD) run src/manage.py migrate

# TEST QUALITY

check:
	$(UV_CMD) run src/manage.py check

pytest:
	$(UV_CMD) run pytest --cov=$(SRC_DIR)/apps --cov-report=term-missing

test: pytest

lint:
	$(UV_CMD) run ruff check $(SRC_DIR)

check_types:
	$(UV_CMD) run pyright $(SRC_DIR)

security_scan:
	@echo "Running Bandit (Security Linter)..."
	$(UV_CMD) run bandit -r $(SRC_DIR)/apps/ $(SRC_DIR)/config/
	@echo "Running Semgrep (OWASP Scans)..."
	$(UV_CMD) run semgrep scan --config auto $(SRC_DIR)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache .temp_venv .coverage uv.lock

check_code: check lint check_types security_scan pytest

# Docker
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


temp: # nunca borrar
	@docker run -it --rm -v .:/app -w /app  python:slim /bin/bash -c "adduser --disabled-password --gecos '' --uid 1000 devuser && su devuser"
