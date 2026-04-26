import hashlib

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.dashboard.models import SubscriptionPlan, UserSettings

User = get_user_model()


class DashboardAccessTests(TestCase):
    def test_dashboard_redirects_anonymous(self):
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 302)  # type: ignore

    def test_profile_redirects_anonymous(self):
        response = self.client.get("/dashboard/profile/")
        self.assertEqual(response.status_code, 302)  # type: ignore

    def test_settings_redirects_anonymous(self):
        response = self.client.get("/dashboard/settings/")
        self.assertEqual(response.status_code, 302)  # type: ignore

    def test_dashboard_accessible_when_logged_in(self):
        password = "testpass123"  # noqa: S105
        user = User.objects.create_user(email="test@example.com", password=password)
        self.client.force_login(user)
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 200)  # type: ignore

    def test_dashboard_home_renders_navigation_shell(self):
        password = "testpass123"  # noqa: S105
        user = User.objects.create_user(email="test@example.com", password=password)
        self.client.force_login(user)
        response = self.client.get("/dashboard/")
        self.assertContains(response, "data-theme")
        self.assertContains(response, "sidebar")
        self.assertContains(response, "Toggle theme")

    def test_settings_page_renders_new_ui_sections(self):
        password = "testpass123"  # noqa: S105
        user = User.objects.create_user(email="test@example.com", password=password)
        self.client.force_login(user)
        response = self.client.get("/dashboard/settings/")
        self.assertContains(response, "Email notifications")
        self.assertContains(response, "API access")
        self.assertContains(response, "Subscription")


class AuthUiSmokeTests(TestCase):
    def test_login_page_uses_modern_shell(self):
        response = self.client.get(reverse("account_login"))
        self.assertEqual(response.status_code, 200)  # type: ignore
        self.assertContains(response, "Sign in")
        self.assertContains(response, "card bg-base-100")

    def test_logout_page_uses_modern_confirmation(self):
        password = "testpass123"  # noqa: S105
        user = User.objects.create_user(email="test@example.com", password=password)
        self.client.force_login(user)
        response = self.client.get(reverse("account_logout"))
        self.assertEqual(response.status_code, 200)  # type: ignore
        self.assertContains(response, "Sign out")
        self.assertContains(response, "end this session")


class SubscriptionPlanModelTests(TestCase):
    def test_create_plan(self):
        plan = SubscriptionPlan.objects.create(
            name="Pro",
            slug="pro",
            description="Pro plan",
            price=9.99,
            interval="monthly",
            features=["API access"],
        )
        self.assertEqual(str(plan), "Pro (Monthly)")
        self.assertTrue(plan.is_active)

    def test_user_settings_created_on_access(self):
        password = "testpass123"  # noqa: S105
        user = User.objects.create_user(email="test@example.com", password=password)
        settings, created = UserSettings.objects.get_or_create(user=user)
        self.assertTrue(created)
        self.assertEqual(settings.subscription_status, "inactive")


class ApiKeyHashingTests(TestCase):
    def setUp(self):
        password = "testpass123"  # noqa: S105
        self.user = User.objects.create_user(
            email="test@example.com",
            password=password,
        )
        self.client.force_login(self.user)

    def test_generate_api_key_stores_only_hash(self):
        self.client.post(reverse("dashboard:generate_api_key"))
        settings = UserSettings.objects.get(user=self.user)
        plaintext = self.client.session["new_api_key"]

        self.assertEqual(len(settings.api_key_hash), 64)
        self.assertNotEqual(settings.api_key_hash, plaintext)
        expected_hash = hashlib.sha256(plaintext.encode()).hexdigest()
        self.assertEqual(settings.api_key_hash, expected_hash)

    def test_api_key_prefix_stored_for_display(self):
        self.client.post(reverse("dashboard:generate_api_key"))
        settings = UserSettings.objects.get(user=self.user)
        plaintext = self.client.session["new_api_key"]

        self.assertEqual(settings.api_key_prefix, plaintext[:8])

    def test_regenerating_key_replaces_hash(self):
        self.client.post(reverse("dashboard:generate_api_key"))
        first_hash = UserSettings.objects.get(user=self.user).api_key_hash

        self.client.post(reverse("dashboard:generate_api_key"))
        second_hash = UserSettings.objects.get(user=self.user).api_key_hash

        self.assertNotEqual(first_hash, second_hash)
