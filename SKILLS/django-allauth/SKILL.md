---
name: django-allauth
description: >
  Django allauth setup, configuration, and template patterns.
  Trigger: When working with django-allauth, authentication, OAuth, or user account management.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

## When to Use

- Setting up user authentication with django-allauth
- Configuring OAuth providers (Google, GitHub, etc.)
- Customizing allauth templates
- Working with email verification and password management
- Implementing social login

## Critical Patterns

### Installation
```bash
pip install django-allauth
```

### Settings Configuration
```python
# settings.py
AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

INSTALLED_APPS = [
    # Native allauth apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # OAuth providers
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
]

# Site ID for allauth
SITE_ID = 1

# Email required
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # or 'optional', 'none'

# Username optional (use email login)
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# Login redirect
LOGIN_REDIRECT_URL = '/dashboard/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
```

### OAuth Providers

**Google** (in `allauth.socialaccount.providers`):
1. Go to Google Cloud Console → APIs & Services → Credentials
2. Create OAuth 2.0 Client ID
3. Add authorized redirect URIs
4. Add to settings:

```python
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': 'YOUR_CLIENT_ID',
            'secret': 'YOUR_CLIENT_SECRET',
            'key': ''
        }
    }
}
```

**GitHub**:
```python
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'APP': {
            'client_id': 'YOUR_CLIENT_ID',
            'secret': 'YOUR_CLIENT_SECRET',
        }
    }
}
```

### Template Structure

Allauth templates go in `templates/account/`:

```
templates/account/
├── base.html           # Base for all account pages
├── auth_base.html      # Base for login/signup pages
├── login.html          # Login form
├── signup.html         # Signup form
├── logout.html         # Logout confirmation
├── password_reset.html # Password reset request
├── password_change.html # Change password
├── email.html          # Email management
├── social_connections.html # OAuth connected accounts
└── verification_sent.html  # Email verification sent
```

### Template Inheritance

```html
{% extends "account/base.html" %}
{% load allauth %}

{% block title %}Login{% endblock %}

{% block content %}
{% element form method="post" action_url=login_url %}
    {% slot body %}
        {% csrf_token %}
        {{ form.as_p }}
    {% endslot %}
    {% slot actions %}
        {% element button type="submit" %}
            {% trans "Sign In" %}
        {% endelement %}
    {% endslot %}
{% endelement %}
{% endblock %}
```

### Using allauth Tags
```html
{% load allauth %}

{# Quick login form #}
{% element form method="post" action_url=login_url %}
    {% slot body %}
        {% csrf_token %}
        {{ form.as_p }}
    {% endslot %}
    {% slot actions %}
        {% element button type="submit" %}Sign In{% endelement %}
    {% endslot %}
{% endelement %}

{# Check if user is authenticated #}
{% if user.is_authenticated %}
    Welcome, {{ user.email }}
{% endif %}

{# OAuth login buttons #}
{% element button href=provider_login_url provider %}
    Sign in with {{ provider.name }}
{% endelement %}
```

### URL Configuration
```python
# urls.py
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('allauth.urls')),
]
```

### Signals for Custom Logic
```python
# signals.py
from allauth.account.signals import user_logged_in, user_signed_up
from django.dispatch import receiver

@receiver(user_logged_in)
def on_user_login(request, user, **kwargs):
    # Custom logic on login
    pass
```

## Commands

```bash
# Create site (run in shell)
from django.contrib.sites.models import Site
Site.objects.update_or_create(id=1, defaults={'domain': 'localhost:8000', 'name': 'localhost'})

# Migrate
python manage.py migrate
```

## Resources

- **allauth docs**: https://docs.allauth.org/
- **Template overrides**: https://docs.allauth.org/en/latest/templates.html
- **OAuth providers**: https://docs.allauth.org/en/latest/socialaccount/providers.html
