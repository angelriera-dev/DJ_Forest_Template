"""
Tests for the User model.

This module contains unit tests for the custom User model.
"""

import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestUserModel:
    """Test suite for User model."""

    def test_create_user_with_email(self):
        """Test creating a user with email as username."""
        user_model = get_user_model()
        password = "testpass123"  # noqa: S105
        user = user_model.objects.create_user(
            email="test@example.com",
            password=password,
        )

        assert user.email == "test@example.com"
        assert user.username == ""
        assert user.check_password(password)
        assert not user.is_staff
        assert user.is_active

    def test_create_user_without_email_raises_error(self):
        """Test that creating a user without email raises ValueError."""
        user_model = get_user_model()
        password = "testpass123"  # noqa: S105

        with pytest.raises(ValueError):
            user_model.objects.create_user(
                email="",
                password=password,
            )

    def test_create_superuser(self):
        """Test creating a superuser."""
        user_model = get_user_model()
        password = "adminpass123"  # noqa: S105
        superuser = user_model.objects.create_superuser(
            email="admin@example.com",
            password=password,
        )

        assert superuser.email == "admin@example.com"
        assert superuser.is_superuser
        assert superuser.is_staff
        assert superuser.is_active

    def test_user_str_returns_email(self):
        """Test that User string representation returns email."""
        user_model = get_user_model()
        user = user_model(email="string@example.com")

        assert str(user) == "string@example.com"

    def test_user_email_is_unique(self):
        """Test that user email must be unique."""
        user_model = get_user_model()
        password = "testpass123"  # noqa: S105
        user_model.objects.create_user(
            email="unique@example.com",
            password=password,
        )

        with pytest.raises(Exception):  # noqa: B017
            user_model.objects.create_user(
                email="unique@example.com",
                password=password,
            )

    def test_user_verbose_names(self):
        """Test verbose names for User model."""
        user_model = get_user_model()
        user = user_model(email="verbose@example.com")

        assert user._meta.verbose_name == "User"
        assert user._meta.verbose_name_plural == "Users"

    def test_user_ordering(self):
        """Test that users are ordered by date_joined descending."""
        user_model = get_user_model()
        password = "pass123"  # noqa: S105

        # Create users in different order
        user_model.objects.create_user(
            email="first@example.com",
            password=password,
        )
        user2 = user_model.objects.create_user(
            email="second@example.com",
            password=password,
        )

        users = list(user_model.objects.all())

        # Second user should be first (newest first)
        assert users[0] == user2

    def test_user_required_fields(self):
        """Test that REQUIRED_FIELDS is empty (email is the only required field)."""
        user_model = get_user_model()

        assert user_model.REQUIRED_FIELDS == ()

    def test_user_username_field(self):
        """Test that USERNAME_FIELD is set to email."""
        user_model = get_user_model()

        assert user_model.USERNAME_FIELD == "email"
