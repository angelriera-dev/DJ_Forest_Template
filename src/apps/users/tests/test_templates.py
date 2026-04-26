"""
Tests for template components and rendering.

Validates that:
- All components render without syntax errors
- Auth templates extend base correctly
- Components receive expected context
"""

import pytest
from django.template import TemplateDoesNotExist
from django.template.loader import get_template


class TestTemplateComponents:
    """Test that all template components exist and load correctly."""

    COMPONENTS = (
        "components/ui/input.html",
        "components/ui/button.html",
        "components/ui/link.html",
        "components/error_block.html",
    )

    @pytest.mark.parametrize("template_path", COMPONENTS)
    def test_component_exists(self, template_path):
        """Each component template should exist and be loadable."""
        try:
            template = get_template(template_path)
            assert template is not None
        except TemplateDoesNotExist:
            pytest.fail(f"Template {template_path} does not exist")

    def test_input_component_renders(self):
        """Input component should render with context."""
        template = get_template("components/ui/input.html")
        rendered = template.render(
            {
                "id": "test_id",
                "name": "test_name",
                "label": "Test Label",
                "placeholder": "Test placeholder",
                "type": "email",
                "required": True,
            }
        )
        assert "test_id" in rendered
        assert "Test Label" in rendered
        assert 'placeholder="Test placeholder"' in rendered

    def test_button_component_renders(self):
        """Button component should render with text."""
        template = get_template("components/ui/button.html")
        rendered = template.render(
            {
                "text": "Submit",
                "icon": "fa-solid fa-check",
            }
        )
        assert "Submit" in rendered
        assert "fa-solid fa-check" in rendered

    def test_link_component_renders(self):
        """Link component should render with url and text."""
        template = get_template("components/ui/link.html")
        # URL tag needs proper context
        rendered = template.render(
            {
                "url": "account_login",
                "text": "Sign in",
            }
        )
        # Note: requires URL resolution which needs request context
        # This test verifies the template syntax is valid
        assert "Sign in" in rendered


class TestAuthTemplates:
    """Test that auth templates load correctly."""

    AUTH_TEMPLATES = (
        "account/login.html",
        "account/signup.html",
        "account/password_reset.html",
    )

    @pytest.mark.parametrize("template_path", AUTH_TEMPLATES)
    def test_auth_template_extends_base(self, template_path):
        """Auth templates should extend base.html."""
        template = get_template(template_path)
        source = template.template.source
        assert 'extends "base.html"' in source

    def test_login_uses_components(self):
        """Login should use input component."""
        template = get_template("account/login.html")
        source = template.template.source
        assert "components/ui/input.html" in source
        assert "components/ui/button.html" in source

    def test_signup_uses_components(self):
        """Signup should use input components."""
        template = get_template("account/signup.html")
        source = template.template.source
        assert "components/ui/input.html" in source


class TestTemplateReduction:
    """Verify template reduction targets are met."""

    def test_login_smaller_than_original(self):
        """Login should be significantly smaller than 69 lines."""
        import os

        template_path = "templates/account/login.html"
        if os.path.exists(template_path):
            with open(template_path) as f:
                lines = len(f.readlines())
            # Original was 69 lines
            assert lines < 50, f"Login is {lines} lines, should be < 50"

    def test_signup_smaller_than_original(self):
        """Signup should be significantly smaller than 60 lines."""
        import os

        template_path = "templates/account/signup.html"
        if os.path.exists(template_path):
            with open(template_path) as f:
                lines = len(f.readlines())
            # Original was 60 lines
            assert lines < 40, f"Signup is {lines} lines, should be < 40"

    def test_password_reset_smaller_than_original(self):
        """Password reset should be significantly smaller than 47 lines."""
        import os

        template_path = "templates/account/password_reset.html"
        if os.path.exists(template_path):
            with open(template_path) as f:
                lines = len(f.readlines())
            # Original was 47 lines
            assert lines < 35, f"Password reset is {lines} lines, should be < 35"
