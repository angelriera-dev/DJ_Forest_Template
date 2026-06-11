# pyright: reportIncompatibleVariableOverride=false, reportMissingTypeArgument=false
from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

if TYPE_CHECKING:
    import apps.users.models

import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.db import models


class UserManager(BaseUserManager):
    """Custom manager for the email-based user model."""

    use_in_migrations = True

    def create_user(
        self: apps.users.models.UserManager,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> User:
        """Create and save a regular user."""
        if not email:
            raise ValueError("The Email address must be set.")

        normalized_email = self.normalize_email(email)
        username = str(extra_fields.pop("username", ""))

        model: Any = self.model  # type: ignore[reportUnknownMemberType]
        user = model(email=normalized_email, username=username, **extra_fields)
        if password is not None:
            validate_password(password, user=user)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self: apps.users.models.UserManager,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ) -> User:
        """Create and save a superuser."""
        extra_fields.setdefault("username", "")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user model that uses email as the primary identifier.

    Inherits from AbstractUser which provides:
    - username (disabled, but kept for Django compatibility)
    - email (our primary USERNAME_FIELD)
    - first_name, last_name
    - is_staff, is_active, is_superuser
    - date_joined, last_login
    - groups, user_permissions
    """

    id: models.UUIDField[Any, Any] = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    # Use email as the unique identifier for authentication
    username: models.CharField[str, str] = models.CharField(
        max_length=150,
        blank=True,
        default="",
        help_text="Optional. 150 characters or fewer.",
    )
    email: models.EmailField[str, str] = models.EmailField(
        unique=True,
        verbose_name="Email address",
        help_text="Required. A valid email address.",
    )

    objects: UserManager = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[tuple[str, ...]] = ()

    class Meta:
        db_table = "users_user"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("-date_joined",)

    def __str__(self: apps.users.models.User) -> str:
        return str(self.email)
