/* "Install Sanatan Saral on your phone" prompt (public site only).
   Android/Chrome: uses the browser's install prompt. iPhone/iPad Safari: shows Share -> Add to Home Screen steps.
   Shown on the 2nd page view (or after 25 s), never when already installed, and stays away 14 days after "Not now". */
(function () {
  var KEY = 'sd-install', DAY = 864e5;
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  var standalone = (window.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone;
  if (standalone) return;
  var snooze = +get(KEY) || 0;
  if (snooze && Date.now() < snooze) return;
  var ua = navigator.userAgent || '';
  var ios = /iPhone|iPad|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var iosSafari = ios && /Safari/.test(ua) && !/CriOS|FxiOS|EdgiOS|GSA|Instagram|FBAN|FBAV|WhatsApp/.test(ua);
  var mobile = ios || /Android/.test(ua);
  if (!mobile) return;
  var views = (+get('sd-views') || 0) + 1; set('sd-views', views);
  var deferred = null, shown = false;
  function hi() { return document.documentElement.getAttribute('data-lang') === 'hi'; }
  function ev(n) { try { gtag('event', n); } catch (e) {} }

  var css = '.ins{position:fixed;left:12px;right:12px;bottom:12px;z-index:60;background:var(--paper,#fff);color:var(--ink,#23363A);border:1.5px solid var(--line,#D5E0DA);border-radius:18px;box-shadow:0 8px 28px rgba(0,0,0,.18);padding:14px 14px 12px;display:flex;gap:12px;align-items:flex-start;max-width:520px;margin:0 auto;font-size:.95rem}' +
    '.ins img{width:44px;height:44px;border-radius:10px;flex-shrink:0}.ins b{display:block;font-size:1rem;margin-bottom:2px}.ins p{margin:0;color:var(--ink-2,#566B6D);line-height:1.4}' +
    '.ins .row{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}.ins button{font:inherit;font-weight:600;border-radius:99px;padding:.5rem 1rem;cursor:pointer;min-height:40px}' +
    '.ins .go{background:var(--indigo,#3C6C72);color:var(--paper,#fff);border:0}.ins .no{background:none;border:1.5px solid var(--line,#D5E0DA);color:var(--ink,#23363A)}' +
    '.ins .share{display:inline-block;vertical-align:-3px;width:16px;height:16px}@media print{.ins{display:none!important}}';

  var SHARE = '<svg class="share" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12M8 7l4-4 4 4"/><path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/></svg>';

  function show() {
    if (shown || document.querySelector('.ins')) return;
    if (!ios && !deferred) return;
    if (ios && !iosSafari) return;
    shown = true;
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    var box = document.createElement('div'); box.className = 'ins'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-label', 'Install Sanatan Saral');
    var body = ios
      ? '<span class="en">Tap ' + SHARE + ' <b style="display:inline">Share</b> below, then <b style="display:inline">Add to Home Screen</b>. It opens like an app, even offline.</span><span class="hi">नीचे ' + SHARE + ' <b style="display:inline">Share</b> दबाएँ, फिर <b style="display:inline">Add to Home Screen</b>। यह ऐप की तरह खुलेगी, ऑफ़लाइन भी।</span>'
      : '<span class="en">Open it like an app from your home screen, even offline. Free, no sign-up.</span><span class="hi">होम स्क्रीन से ऐप की तरह खोलें, ऑफ़लाइन भी। निःशुल्क, कोई साइन-अप नहीं।</span>';
    box.innerHTML = '<img src="/icon-192.png" alt="">' +
      '<div><b><span class="en">Install Sanatan Saral on your phone</span><span class="hi">सनातन सरल को अपने फ़ोन में जोड़ें</span></b><p>' + body + '</p>' +
      '<div class="row">' + (ios ? '' : '<button type="button" class="go"><span class="en">Install</span><span class="hi">जोड़ें</span></button>') +
      '<button type="button" class="no"><span class="en">' + (ios ? 'Got it' : 'Not now') + '</span><span class="hi">' + (ios ? 'ठीक है' : 'अभी नहीं') + '</span></button></div></div>';
    document.body.appendChild(box);
    ev('install_prompt_shown');
    var close = function (n) { box.remove(); set(KEY, String(Date.now() + n * DAY)); };
    box.querySelector('.no').onclick = function () { ev('install_prompt_dismissed'); close(14); };
    var go = box.querySelector('.go');
    if (go) go.onclick = function () {
      ev('install_prompt_clicked');
      deferred.prompt();
      deferred.userChoice.then(function (c) { if (c && c.outcome === 'accepted') ev('app_installed'); close(c && c.outcome === 'accepted' ? 3650 : 14); deferred = null; });
    };
  }

  window.addEventListener('beforeinstallprompt', function (e) { e.preventDefault(); deferred = e; if (views >= 2) setTimeout(show, 4000); });
  window.addEventListener('appinstalled', function () { ev('app_installed'); set(KEY, String(Date.now() + 3650 * DAY)); var b = document.querySelector('.ins'); if (b) b.remove(); });
  if (views >= 2) setTimeout(show, ios ? 4000 : 6000);
  else setTimeout(show, 25000);
})();
