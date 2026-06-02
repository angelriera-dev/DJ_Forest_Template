from __future__ import annotations

from typing import Any

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class SubscriptionPlan(BaseModel):
    name: models.CharField[str, str] = models.CharField(max_length=100)
    slug: models.SlugField[str, str] = models.SlugField(unique=True)
    description: models.TextField[str, str] = models.TextField()
    price: models.DecimalField[Any, Any] = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    interval: models.CharField[str, str] = models.CharField(
        max_length=20,
        choices=[
            ("monthly", "Monthly"),
            ("yearly", "Yearly"),
        ],
        default="monthly",
    )
    features: models.JSONField[Any, Any] = models.JSONField(default=list)
    is_active: models.BooleanField[bool, bool] = models.BooleanField(default=True)

    class Meta(BaseModel.Meta):
        verbose_name = "Subscription Plan"
        verbose_name_plural = "Subscription Plans"

    def __str__(self) -> str:
        # Cast para evitar error de tipado en acceso dinámico
        interval = str(self.get_interval_display())  # type: ignore
        return f"{self.name} ({interval})"


class UserSettings(BaseModel):
    user: models.OneToOneField[Any, Any] = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="settings"
    )

    # Notification preferences
    notify_comments: models.BooleanField[bool, bool] = models.BooleanField(
        default=False
    )
    notify_updates: models.BooleanField[bool, bool] = models.BooleanField(default=False)
    notify_marketing: models.BooleanField[bool, bool] = models.BooleanField(
        default=False
    )

    # Subscription settings
    subscription_plan: models.ForeignKey[Any, Any] = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subscribers",
    )
    subscription_status: models.CharField[str, str] = models.CharField(
        max_length=20,
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("cancelled", "Cancelled"),
            ("trial", "Trial"),
        ],
        default="inactive",
    )
    subscription_start_date: models.DateTimeField[Any, Any] = models.DateTimeField(
        null=True, blank=True
    )
    subscription_end_date: models.DateTimeField[Any, Any] = models.DateTimeField(
        null=True, blank=True
    )
    trial_end_date: models.DateTimeField[Any, Any] = models.DateTimeField(
        null=True, blank=True
    )
    api_key_hash: models.CharField[str, str] = models.CharField(
        max_length=64, blank=True, default=""
    )
    api_key_prefix: models.CharField[str, str] = models.CharField(
        max_length=8, blank=True, default=""
    )
    api_key_created_at: models.DateTimeField[Any, Any] = models.DateTimeField(
        null=True, blank=True
    )

    class Meta(BaseModel.Meta):
        verbose_name = "User Settings"
        verbose_name_plural = "User Settings"

    def __str__(self) -> str:
        user_email = getattr(self.user, "email", "Unknown")
        return f"Settings for {user_email}"

    @property
    def is_subscription_active(self) -> bool:
        if self.subscription_status != "active":
            return False
        if self.subscription_end_date and self.subscription_end_date < timezone.now():
            return False
        return True

    @property
    def is_trial_active(self) -> bool:
        if self.subscription_status != "trial":
            return False
        if self.trial_end_date and self.trial_end_date < timezone.now():
            return False
        return True
