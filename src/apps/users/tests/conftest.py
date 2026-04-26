"""
Pytest fixtures for users app tests.

This file provides reusable test fixtures for the users application.
"""

import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def user(db):
    """
    Create a regular user for testing.

    Returns:
        User: A User instance with default password (unusable).
    """
    user_model = get_user_model()
    user_instance = user_model(
        email="testuser@example.com",
        first_name="Test",
        last_name="User",
    )
    user_instance.set_password("testpass123")
    user_instance.save()
    return user_instance


@pytest.fixture
def superuser(db):
    """
    Create a superuser for testing.

    Returns:
        User: A superuser instance with all permissions.
    """
    user_model = get_user_model()
    user_instance = user_model(
        email="admin@example.com",
        is_staff=True,
        is_superuser=True,
    )
    user_instance.set_password("adminpass123")
    user_instance.save()
    return user_instance


@pytest.fixture
def user_data():
    """
    Return dictionary of user data for creating users.

    Returns:
        dict: User data dictionary.
    """
    return {
        "email": "newuser@example.com",
        "password": "newpass123",
        "first_name": "New",
        "last_name": "User",
    }


@pytest.fixture
def authenticated_client(client, user):
    """
    Create an authenticated client for testing.

    Returns:
        HttpClient: An authenticated Django test client.
    """
    client.force_login(user)
    return client


@pytest.fixture
def api_client():
    """
    Create an API client for testing DRF endpoints.

    Returns:
        APIClient: A DRF API test client.
    """
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def authenticated_api_client(api_client, user):
    """
    Create an authenticated API client for testing.

    Returns:
        APIClient: An authenticated DRF API test client.
    """
    api_client.force_authenticate(user=user)
    return api_client
