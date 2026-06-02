from __future__ import annotations

import uuid
from typing import Any

from django.db import models
from django.utils import timezone


class RegisterModel(models.Model):
    create_at: models.DateTimeField[Any, Any] = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField[Any, Any] = models.DateTimeField(auto_now=True)
    deleted_at: models.DateTimeField[Any, Any] = models.DateTimeField(
        null=True, blank=True
    )

    def __str__(self) -> str:
        return str(self.updated_at)


class BaseModel(models.Model):
    id: models.UUIDField[Any, Any] = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    create_at: models.DateTimeField[Any, Any] = models.DateTimeField(
        default=timezone.now
    )
    updated_at: models.DateTimeField[Any, Any] = models.DateTimeField(auto_now=True)
    deleted_at: models.DateTimeField[Any, Any] = models.DateTimeField(
        null=True, blank=True
    )

    class Meta:
        abstract = True
        ordering = ("-create_at",)
