

NAV_LINKS = [
    {"name": "Dashboard", "url": "dashboard:home", "icon": "🏠"},
    { "name": "Edit profile", "url": "dashboard:profile", "icon": "👤", },
    { "name": "Settings", "url": "dashboard:settings", "icon": "⚙️", },
    { "name": "Upgrade plan", "url": "dashboard:subscription_plans", "icon": "💳" },


]
def navigation(request):
    return {'nav_items': NAV_LINKS}
