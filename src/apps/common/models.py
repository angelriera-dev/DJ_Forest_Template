import uuid

from django.db import models


class RegisterModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.updated_at)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    register = models.OneToOneField(
        RegisterModel, on_delete=models.CASCADE, parent_link=True
    )

    class Meta:
        abstract = True
        ordering = ("-create_at",)
