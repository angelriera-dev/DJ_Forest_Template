---
name: htmx-patterns
description: >
  HTMX advanced patterns: swap modifiers, events, OOB updates, indicators.
  Trigger: When working with HTMX swap, events, loading states, or complex HTMX interactions.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

## When to Use

- Implementing HTMX swap modifiers (innerHTML, beforeend, etc.)
- Using HTMX events for lifecycle management
- Out-of-band (OOB) updates
- Loading indicators and UX
- Boosted navigation
- SSE (Server-Sent Events) with HTMX
- WebSocket integration

## Critical Patterns

### Swap Modifiers

| Modifier | Behavior | Use Case |
|----------|----------|----------|
| `outerHTML` (default) | Replace entire element | Most common |
| `innerHTML` | Replace inner content only | Content updates |
| `beforeend` | Append to end | Infinite scroll, lists |
| `afterbegin` | Prepend to start | Chat messages, feeds |
| `beforebegin` | Insert before element | Insertion at position |
| `afterend` | Insert after element | Insertion at position |
| `delete` | Remove element | Delete confirmation |
| `none` | No swap | Events only |

```html
<!-- Append new item to list -->
<div hx-get="/more-items" hx-trigger="revealed" hx-swap="beforeend">
    <!-- items load here -->
</div>

<!-- Replace only content, keep container -->
<div id="comments">
    <div hx-get="/comments" hx-swap="innerHTML">
        {{ comments }}
    </div>
</div>
```

### HTMX Events

**Lifecycle Events**:
```javascript
document.addEventListener('htmx:load', function(evt) {
    // Element initialized
});

document.addEventListener('htmx:afterSwap', function(evt) {
    // Content swapped into DOM - reinitialize any JS
});

document.addEventListener('htmx:beforeRequest', function(evt) {
    // Before HTMX request
});

document.addEventListener('htmx:afterRequest', function(evt) {
    // After request completes (success or error)
});

document.addEventListener('htmx:responseError', function(evt) {
    // 4xx or 5xx response
});
```

**Custom Events** (from server):
```python
# Django view can trigger events
response['HX-Trigger'] = json.dumps({'showMessage': {'message': 'Saved!'}})
```

```javascript
document.addEventListener('showMessage', function(evt) {
    alert(evt.detail.message);
})
```

**Trigger Filters**:
```html
<!-- Only trigger on enter key -->
<input hx-get="/search" hx-trigger="keyup changed delay:300ms, enter">

<!-- Trigger on click, but not on shift+click -->
<button hx-delete="/item" hx-trigger="click[!event.shiftKey]">

<!-- Once per session -->
<button hx-get="/init" hx-trigger="once">
```

### Out-of-Band (OOB) Updates

Send multiple element updates in one response:

```html
<!-- Server returns this response -->
<div id="sidebar" hx-swap-oob="true">
    {% include "partials/sidebar.html" %}
</div>
<div id="cart-count" hx-swap-oob="true">
    {{ cart_items.count }}
</div>
<article id="new-item">
    <!-- Main content -->
</article>
```

**Django example**:
```python
def add_item(request):
    # ... save item ...

    # Build OOB response
    response = render(request, 'partials/new_item.html', {'item': item})
    response['HX-Trigger'] = json.dumps({
        'itemAdded': {'id': item.id},
        'updateCartCount': {'count': Cart.objects.count()}
    })

    # OOB targets in response body
    return response
```

### Loading Indicators

**Simple approach**:
```html
<button hx-get="/data" hx-indicator="#loading">
    Load Data
</button>
<span id="loading" class="htmx-indicator">Loading...</span>

<style>
.htmx-indicator { display: none; }
.htmx-request .htmx-indicator { display: inline; }
.htmx-request.htmx-indicator { display: inline; }
</style>
```

**With Alpine.js**:
```html
<div x-data="{ loading: false }"
     @htmx:beforeRequest="loading = true"
     @htmx:afterRequest="loading = false">
    <button hx-get="/data" :disabled="loading">
        <span x-show="loading">Loading...</span>
        <span x-show="!loading">Load</span>
    </button>
</div>
```

**Request class on parent**:
```html
<div class="hx-request" hx-get="/data" hx-target="#results">
    <div id="results"></div>
</div>

<style>
:not(.hx-request) .loading-skeleton { display: none; }
.hx-request .loading-skeleton { display: block; }
</style>
```

### Boosted Navigation

Turn regular links into HTMX:
```html
<!-- Add to head -->
<script src="https://unpkg.com/htmx.org/dist/htmx.js"></script>
<script>
    htmx.configboost = true;  // Enable boosting
</script>

<!-- Boosted link -->
<a href="/page" hx-boost="true">Page</a>
```

This converts links/forms to HTMX GET/POST, swaps content smoothly.

### SSE (Server-Sent Events)

```html
<div hx-get="/events" hx-trigger="sse:/topic">
    <div id="messages"></div>
</div>
```

```python
# Django view
def events(request):
    response = StreamingHttpResponse(
        event_stream(),
        content_type='text/event-stream'
    )
    response['Cache-Control'] = 'no-cache'
    return response

def event_stream():
    pubsub = redis.pubsub()
    pubsub.subscribe('topic')
    for message in pubsub.listen():
        if message['type'] == 'message':
            yield f"data: {message['data']}\n\n"
```

### WebSocket Integration

```html
<div hx-ws="connect:/ws/chat">
    <div id="messages"></div>
    <form hx-ws="submit:closest form">
        <input name="message" type="text">
        <button>Send</button>
    </form>
</div>
```

### Advanced: History API

```html
<!-- Save navigation history -->
<a href="/page" hx-boost="true" hx-history-elt="true">

<!-- Restore on back button -->
<script>
    htmx.config.historyCacheSize = 20;
    htmx.config.refreshOnHistoryMiss = true;
</script>
```

## Commands

```bash
# Install django-htmx for server-side helpers
pip install django-htmx
```

```python
# settings.py
INSTALLED_APPS = ['django_htmx']
MIDDLEWARE = ['django_htmx.middleware.HTMXMiddleware']
```

## Resources

- **HTMX Events**: https://htmx.org/reference/events/
- **HTMX Attributes**: https://htmx.org/reference/attributes/
- **SSE Extension**: https://htmx.org/extensions/sse/
- **WebSocket Extension**: https://htmx.org/extensions/ws/
