---
name: django-htmx
description: >
  Django + HTMX + Alpine.js patterns for modern SaaS applications.
  Trigger: When working with Django templates, HTMX requests, or HTMX+Alpine.js interactivity.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

## When to Use

- Creating Django views that return HTMX responses
- Building reusable components with partial templates
- Adding reactivity with Alpine.js alongside HTMX
- Working with Django forms and HTMX form handling
- Implementing Django-allauth templates

## Critical Patterns

### HTMX Response Pattern
Always return partials for HTMX requests, full page for regular requests:

```python
def my_view(request):
    if request.headers.get('HX-Request'):
        return render(request, 'partials/my-component.html', {...})
    return render(request, 'full-page.html', {...})
```

### Reusable Components
Extract to `templates/components/{component-name}.html`:

```
templates/components/
├── modal.html
├── button.html
├── form_field.html
├── card_stat.html
└── quick_actions.html
```

Include with: `{% include "components/modal.html" with id="x" title="y" %}`

### CSRF in Forms
Always include CSRF token in HTMX forms:

```html
<form hx-post="{% url 'my-url' %}">
    {% csrf_token %}
    <!-- fields -->
</form>
```

### HTMX + Alpine.js Combo
Alpine `x-data` must be on parent element:

```html
<div x-data="{ open: false }">
    <button @click="open = true">Open</button>
    <div x-show="open" hx-get="/endpoint" hx-trigger="open">
        Content loaded via HTMX
    </div>
</div>
```

### HTMX Swap Modifiers
Use swap modifiers for fine-grained control:

| Modifier | Use Case |
|----------|----------|
| `hx-swap="outerHTML"` | Replace entire element (default) |
| `hx-swap="innerHTML"` | Replace inner content only |
| `hx-swap="beforeend"` | Append to element |
| `hx-swap="afterbegin"` | Prepend to element |
| `hx-swap="delete"` | Remove element after swap |

### Loading States
Show loading indicators:

```html
<img hx-get="/image" hx-indicator="#loading" src="placeholder.jpg">
<span id="loading" class="htmx-indicator">Loading...</span>
```

CSS:
```css
.htmx-indicator { display: none; }
.htmx-request .htmx-indicator { display: inline; }
.htmx-request.htmx-indicator { display: inline; }
```

### HTMX Events
Listen for lifecycle events:

| Event | When |
|-------|------|
| `htmx:load` | Element initialized |
| `htmx:afterSwap` | Content swapped into DOM |
| `htmx:beforeRequest` | Before request sent |
| `htmx:afterRequest` | After request completes |
| `htmx:responseError` | On 4xx/5xx response |

### View Decorators
Use `require_htmx` for HTMX-only views:

```python
from django_htmx.middleware import require_htmx

@require_htmx
def htmx_only_view(request):
    ...
```

## Component Examples

### Modal Component
```html
{% load django_htmx %}
<input type="checkbox" id="{{ id|default:"modal" }}" class="modal-toggle" />
<div class="modal" role="dialog">
  <div class="modal-box">
    {% if title %}<h3 class="font-bold text-lg">{{ title }}</h3>{% endif %}
    <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
            onclick="this.closest('.modal').querySelector('input').checked = false">✕</button>
    <div class="py-4">{{ content }}</div>
    {% if actions %}<div class="modal-action">{{ actions }}</div>{% endif %}
  </div>
  <label class="modal-backdrop bg-black/50"></label>
</div>
```

### Button with HTMX
```html
<button hx-get="{{ url }}"
        hx-target="#target"
        hx-swap="outerHTML"
        hx-indicator="#loading"
        class="btn btn-primary">
    <span class="htmx-indicator">Loading...</span>
    <span>Click Me</span>
</button>
```

## Commands

```bash
# Install django-htmx
pip install django-htmx

# Add to settings.py
INSTALLED_APPS = ['django_htmx']
MIDDLEWARE = ['django_htmx.middleware.HTMXMiddleware']
```

## Resources

- **Django HTMX GitHub**: https://github.com/adamchainz/django-htmx
- **HTMX Docs**: https://htmx.org/docs/
- **Alpine.js Docs**: https://alpinejs.dev/start
- **DaisyUI**: https://daisyui.com/
- **django-widget-tweaks**: https://github.com/jazzband/django-widget-tweaks
- **Tailwind CSS**: https://tailwindcss.com/
- **django-tailwind**: https://github.com/timonweb/django-tailwind
