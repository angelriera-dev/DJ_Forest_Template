// Alpine component definitions — must load BEFORE Alpine initializes
// Loaded with defer so Alpine CDN and this file race is resolved by alpine:init event

document.addEventListener('alpine:init', function () {
    Alpine.data('app', function () {
        return {
            init: function () {
                var self = this;
                document.body.addEventListener('htmx:responseError', function (evt) {
                    self.notify('Server error: ' + evt.detail.xhr.statusText, 'error');
                });
                document.body.addEventListener('htmx:beforeSwap', function (evt) {
                    if (evt.detail.xhr.status === 422) {
                        evt.detail.shouldSwap = true;
                        evt.detail.isError = false;
                    }
                });
            },
            notifications: [],
            notify: function (text, type) {
                type = type || 'info';
                var id = Date.now();
                this.notifications.push({ id: id, text: text, type: type });
                var self = this;
                setTimeout(function () {
                    self.notifications = self.notifications.filter(function (n) { return n.id !== id; });
                }, 5000);
            }
        };
    });

    Alpine.data('ttsComponent', function () {
        return {
            playing: false,
            loading: false,
            handleClick: function () {
                this.playing ? this.stop() : this.play();
            },
            play: function () {
                var text = this.$el.getAttribute('data-text');
                if (!text) return;
                this.loading = true;
                window.speechSynthesis.cancel();
                var utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 0.9;
                utterance.pitch = 1;
                utterance.lang = /[áéíóúñü¿¡]/i.test(text) ? 'es-ES' : 'en-US';
                var self = this;
                utterance.onstart = function () { self.loading = false; self.playing = true; };
                utterance.onend = function () { self.playing = false; self.loading = false; };
                utterance.onerror = function () { self.playing = false; self.loading = false; };
                window.speechSynthesis.speak(utterance);
            },
            stop: function () {
                window.speechSynthesis.cancel();
                this.playing = false;
                this.loading = false;
            }
        };
    });
});
