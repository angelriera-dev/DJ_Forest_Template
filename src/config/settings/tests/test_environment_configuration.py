"""Environment settings are exercised in fresh processes to isolate imports."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[3]


def run_settings(env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    process_env = {
        key: value
        for key, value in os.environ.items()
        if key.startswith(("PATH", "SYSTEMROOT", "WINDIR"))
    }
    process_env.update(env)
    process_env["PYTHONPATH"] = str(SRC_DIR)
    process_env["DJANGO_SETTINGS_MODULE"] = f"config.settings.{env['DJANGO_ENV']}"
    code = (
        "import json; from django.conf import settings; "
        "db = settings.DATABASES['default']; "
        "print(json.dumps({'debug': settings.DEBUG, 'engine': db['ENGINE'], "
        "'name': str(db['NAME']), 'host': db.get('HOST'), "
        "'options': db.get('OPTIONS', {}), 'hosts': settings.ALLOWED_HOSTS, "
        "'csrf': settings.CSRF_TRUSTED_ORIGINS, "
        "'ssl_redirect': settings.SECURE_SSL_REDIRECT, "
        "'session_cookie_secure': settings.SESSION_COOKIE_SECURE}))"
    )
    return subprocess.run(
        [sys.executable, "-c", code],
        check=False,
        capture_output=True,
        text=True,
        env=process_env,
        cwd=SRC_DIR.parent,
    )


def run_entrypoint(
    env: dict[str, str], module: str
) -> subprocess.CompletedProcess[str]:
    process_env = {
        key: value
        for key, value in os.environ.items()
        if key.startswith(("PATH", "SYSTEMROOT", "WINDIR"))
    }
    process_env.update(env)
    process_env["PYTHONPATH"] = str(SRC_DIR)
    code = (
        f"import json, {module}; from django.conf import settings; "
        "print(json.dumps({'debug': settings.DEBUG, "
        "'name': settings.DATABASES['default']['NAME']}))"
    )
    return subprocess.run(
        [sys.executable, "-c", code],
        check=False,
        capture_output=True,
        text=True,
        env=process_env,
        cwd=SRC_DIR.parent,
    )


def local_env(environment: str) -> dict[str, str]:
    return {
        "DJANGO_ENV": environment,
        "DJANGO_SECRET_KEY": "django-insecure-dev-only-change-me",
        "DB_NAME": f"django_{environment}",
        "DB_USER": f"django_{environment}",
        "DB_PASSWORD": "local-only-password",
        "DB_HOST": "db",
        "DB_PORT": "5432",
        "ALLOWED_HOSTS": "localhost,127.0.0.1",
        "CSRF_TRUSTED_ORIGINS": "http://localhost:8000",
    }


def test_wsgi_and_asgi_select_environment_settings_from_django_env() -> None:
    for module in ("config.wsgi", "config.asgi"):
        result = run_entrypoint(local_env("staging"), module)

        assert result.returncode == 0, result.stderr
        settings = json.loads(result.stdout)
        assert settings == {"debug": False, "name": "django_staging"}


def test_dev_uses_postgres_and_keeps_local_debug_enabled() -> None:
    result = run_settings(local_env("dev"))

    assert result.returncode == 0, result.stderr
    settings = json.loads(result.stdout)
    assert settings["debug"] is True
    assert settings["engine"] == "django.db.backends.postgresql"
    assert settings["name"] == "django_dev"
    assert settings["hosts"] == ["*"]


def test_staging_is_non_debug_and_accepts_local_postgres() -> None:
    result = run_settings(local_env("staging"))

    assert result.returncode == 0, result.stderr
    settings = json.loads(result.stdout)
    assert settings["debug"] is False
    assert settings["engine"] == "django.db.backends.postgresql"
    assert settings["name"] == "django_staging"
    assert settings["ssl_redirect"] is False
    assert settings["session_cookie_secure"] is False


def test_production_rejects_missing_required_security_configuration() -> None:
    env = local_env("prod")
    env["DJANGO_SECRET_KEY"] = ""
    env["ALLOWED_HOSTS"] = ""
    env["CSRF_TRUSTED_ORIGINS"] = ""

    result = run_settings(env)

    assert result.returncode != 0
    assert "DJANGO_SECRET_KEY" in result.stderr


@pytest.mark.parametrize(
    ("missing_variable", "expected_error"),
    [
        ("ALLOWED_HOSTS", "requires explicit ALLOWED_HOSTS"),
        ("CSRF_TRUSTED_ORIGINS", "requires explicit CSRF_TRUSTED_ORIGINS"),
    ],
)
def test_production_requires_explicit_host_and_csrf_configuration(
    missing_variable: str, expected_error: str
) -> None:
    env = local_env("prod")
    env["DJANGO_SECRET_KEY"] = (
        "production-only-secret-key-with-enough-entropy-and-required-length-2026"
    )
    env[missing_variable] = ""

    result = run_settings(env)

    assert result.returncode != 0
    assert expected_error in result.stderr


def test_production_rejects_short_secret_key() -> None:
    env = local_env("prod")
    env["DJANGO_SECRET_KEY"] = "too-short"

    result = run_settings(env)

    assert result.returncode != 0
    assert "at least 50 characters" in result.stderr


def test_non_development_database_url_rejects_disabled_tls() -> None:
    env = local_env("staging")
    env["DJANGO_SECRET_KEY"] = (
        "staging-cloud-test-secret-with-sufficient-length-and-entropy"
    )
    env["DATABASE_URL"] = (
        "postgres://cloud-user:cloud-pass@db.example.test/app?sslmode=disable"
    )

    result = run_settings(env)

    assert result.returncode != 0
    assert "must enable PostgreSQL TLS" in result.stderr


def test_production_rejects_wildcard_hosts() -> None:
    env = local_env("prod")
    env["DJANGO_SECRET_KEY"] = (
        "production-only-secret-key-with-enough-entropy-and-required-length-2026"
    )
    env["ALLOWED_HOSTS"] = "*"

    result = run_settings(env)

    assert result.returncode != 0
    assert "wildcard hosts are not allowed" in result.stderr


def test_cloud_staging_rejects_the_local_example_secret() -> None:
    env = local_env("staging")
    env["DATABASE_URL"] = "postgres://cloud-user:cloud-pass@db.example.test/app"

    result = run_settings(env)

    assert result.returncode != 0
    assert "DJANGO_SECRET_KEY" in result.stderr


def test_cloud_staging_database_url_does_not_enable_https_for_local_app() -> None:
    env = local_env("staging")
    env["DJANGO_SECRET_KEY"] = (
        "staging-cloud-test-secret-with-sufficient-length-and-entropy"
    )
    env["DATABASE_URL"] = "postgres://cloud-user:cloud-pass@db.example.test/app"

    result = run_settings(env)

    assert result.returncode == 0, result.stderr
    settings = json.loads(result.stdout)
    assert settings["host"] == "db.example.test"
    assert settings["ssl_redirect"] is False
    assert settings["session_cookie_secure"] is False


def test_staging_https_requires_explicit_proxy_deployment_setting() -> None:
    env = local_env("staging")
    env["DJANGO_SECRET_KEY"] = (
        "staging-cloud-test-secret-with-sufficient-length-and-entropy"
    )
    env["DATABASE_URL"] = "postgres://cloud-user:cloud-pass@db.example.test/app"
    env["DJANGO_SECURE_SSL_REDIRECT"] = "true"

    result = run_settings(env)

    assert result.returncode == 0, result.stderr
    settings = json.loads(result.stdout)
    assert settings["ssl_redirect"] is True
    assert settings["session_cookie_secure"] is True


def test_production_uses_database_url_and_enforces_secure_cookies() -> None:
    env = local_env("prod")
    env["DJANGO_SECRET_KEY"] = (
        "production-only-secret-key-with-enough-entropy-and-required-length-2026"
    )
    env["DATABASE_URL"] = "postgres://app:db-pass@db.example.test/app"

    result = run_settings(env)

    assert result.returncode == 0, result.stderr
    settings = json.loads(result.stdout)
    assert settings["debug"] is False
    assert settings["engine"] == "django.db.backends.postgresql"
    assert settings["host"] == "db.example.test"
    assert settings["options"]["sslmode"] == "require"
    assert settings["ssl_redirect"] is True
    assert settings["session_cookie_secure"] is True
