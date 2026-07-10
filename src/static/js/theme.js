// Theme bootstrap — runs immediately in <head>, no defer, no Alpine dependency
// ponytail: localStorage only; add server-side persistence when user prefs are needed across devices
(function () {
    // 1. Restore light/dark mode
    var saved = localStorage.getItem('theme') ||
        (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', saved);

    // 2. Restore custom color variables
    ['primary', 'secondary', 'accent'].forEach(function (key) {
        var val = localStorage.getItem('color-' + key);
        if (val) document.documentElement.style.setProperty('--color-' + key, val);
    });

    // 3. Wire theme-controller checkbox and color pickers once DOM is ready
    document.addEventListener('DOMContentLoaded', function () {
        // Sync the navbar toggle checkbox with saved state
        document.querySelectorAll('.theme-controller').forEach(function (ctrl) {
            ctrl.checked = saved === 'dark';
            ctrl.addEventListener('change', function () {
                saved = ctrl.checked ? 'dark' : 'light';
                localStorage.setItem('theme', saved);
                document.documentElement.setAttribute('data-theme', saved);
                // Keep all other theme-controller checkboxes in sync
                document.querySelectorAll('.theme-controller').forEach(function (other) {
                    other.checked = ctrl.checked;
                });
            });
        });

        // Color picker — only active on /settings/
        ['primary', 'secondary', 'accent'].forEach(function (key) {
            var input = document.getElementById('color-' + key);
            if (!input) return;

            var current = localStorage.getItem('color-' + key) ||
                getComputedStyle(document.documentElement).getPropertyValue('--color-' + key).trim();
            if (current) input.value = current;

            input.addEventListener('input', function () {
                document.documentElement.style.setProperty('--color-' + key, input.value);
                localStorage.setItem('color-' + key, input.value);
            });
        });

        var resetBtn = document.getElementById('reset-colors');
        if (resetBtn) {
            resetBtn.addEventListener('click', function () {
                ['primary', 'secondary', 'accent'].forEach(function (key) {
                    document.documentElement.style.removeProperty('--color-' + key);
                    localStorage.removeItem('color-' + key);
                    var input = document.getElementById('color-' + key);
                    if (input) {
                        input.value = getComputedStyle(document.documentElement)
                            .getPropertyValue('--color-' + key).trim();
                    }
                });
            });
        }
    });
})();
