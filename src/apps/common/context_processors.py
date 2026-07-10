from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import django.core.handlers.wsgi
NAV_LINKS = [
    {"name": "Dashboard", "url": "dashboard:home", "icon": "🏠"},
    {
        "name": "Edit profile",
        "url": "dashboard:profile",
        "icon": "👤",
    },
    {
        "name": "Settings",
        "url": "dashboard:settings",
        "icon": "⚙️",
    },
    {"name": "Upgrade plan", "url": "dashboard:subscription_plans", "icon": "💳"},
]


def navigation(
    request: "django.core.handlers.wsgi.WSGIRequest",
) -> dict[str, list[dict[str, str]]]:
    return {"nav_items": NAV_LINKS}
