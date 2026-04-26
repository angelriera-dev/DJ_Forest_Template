from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configuration for the users app."""

    default_auto_field = "django.db.models.BigAutoField"  # type: ignore
    name = "apps.users"
    verbose_name = "Users"
