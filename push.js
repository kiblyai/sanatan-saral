/* "Daily shloka on your phone": web-push subscribe button (public site only).
   The Cloudflare Worker at API stores the subscription and sends one wake-up push a day;
   the service worker then shows that day's entry from /push/<month>.json. */
(function () {
  var API = '';  // set to the Worker's URL once it exists, e.g. 'https://sanatan-push.<name>.workers.dev'
  var PUB = 'BFuqhBj3vBLmmnDqfOSSxFrdBcag3H8R14nSnJQKIuzVyV6icygZFrIME_hnesj1i4PGgXytADTFLLWJuV30ZmQ';
  if (!API || !('serviceWorker' in navigator) || !('PushManager' in window) || !('Notification' in window)) return;
  var ua = navigator.userAgent || '';
  var ios = /iPhone|iPad|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var standalone = (window.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone;
  if (ios && !standalone) return;  // iPhone allows notifications only for sites added to the home screen
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function ev(n) { try { gtag('event', n); } catch (e) {} }
  function lang() { return document.documentElement.getAttribute('data-lang') === 'hi' ? 'hi' : 'en'; }
  function key(b) { var p = '='.repeat((4 - b.length % 4) % 4), s = atob((b + p).replace(/-/g, '+').replace(/_/g, '/')), a = new Uint8Array(s.length); for (var i = 0; i < s.length; i++) a[i] = s.charCodeAt(i); return a; }
  function tellLang() { navigator.serviceWorker.ready.then(function (r) { if (r.active) r.active.postMessage({ type: 'lang', lang: lang() }); }); }

  var st = document.createElement('style');
  st.textContent = '.pushb{font:inherit;font-weight:600;font-size:.92rem;border:1.5px solid var(--line,#D5E0DA);background:var(--paper,#fff);color:var(--ink,#23363A);border-radius:99px;padding:.45rem .95rem;cursor:pointer;min-height:40px;margin:.6rem 0}.pushb[aria-pressed="true"]{border-color:var(--indigo,#3C6C72)}.push-card{position:fixed;left:12px;right:12px;bottom:12px;z-index:60;max-width:520px;margin:0 auto;background:var(--paper,#fff);color:var(--ink,#23363A);border:1.5px solid var(--line,#D5E0DA);border-radius:18px;box-shadow:0 8px 28px rgba(0,0,0,.18);padding:14px}.push-card b{display:block;margin-bottom:4px}.push-card p{margin:0 0 10px;color:var(--ink-2,#566B6D)}.push-card .no{font:inherit;background:none;border:0;color:var(--ink-2,#566B6D);cursor:pointer;margin-left:6px;min-height:40px}@media print{.pushb,.push-card{display:none!important}}';
  document.head.appendChild(st);

  var buttons = [];
  function label(on) { return on ? '<span class="en">🔔 Daily shloka is on · turn off</span><span class="hi">🔔 दैनिक श्लोक चालू है · बन्द करें</span>' : '<span class="en">🔔 Get a daily shloka on your phone</span><span class="hi">🔔 फ़ोन पर रोज़ एक श्लोक पाएँ</span>'; }
  function paint(on) { buttons.forEach(function (b) { b.innerHTML = label(on); b.setAttribute('aria-pressed', on ? 'true' : 'false'); }); }
  function current() { return navigator.serviceWorker.ready.then(function (r) { return r.pushManager.getSubscription(); }); }

  function turnOn() {
    return Notification.requestPermission().then(function (p) {
      if (p !== 'granted') { alertLine(false); return; }
      return navigator.serviceWorker.ready.then(function (r) { return r.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: key(PUB) }); })
        .then(function (sub) { return fetch(API + '/subscribe', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ endpoint: sub.endpoint }) }); })
        .then(function () { tellLang(); paint(true); ev('push_subscribed'); set('sd-push-asked', '1'); });
    }).catch(function () { alertLine(false); });
  }
  function turnOff() {
    return current().then(function (sub) {
      if (!sub) return;
      fetch(API + '/unsubscribe', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ endpoint: sub.endpoint }) }).catch(function () {});
      return sub.unsubscribe();
    }).then(function () { paint(false); ev('push_unsubscribed'); });
  }
  function alertLine() {
    buttons.forEach(function (b) { var n = b.nextElementSibling; if (n && n.className === 'push-note') return; n = document.createElement('p'); n.className = 'push-note'; n.style.cssText = 'font-size:.88rem;color:var(--ink-2,#566B6D);margin:.2rem 0'; n.innerHTML = '<span class="en">Notifications are blocked. Allow them for this site in your phone settings, then try again.</span><span class="hi">सूचनाएँ बन्द हैं। फ़ोन की सेटिंग में इस साइट के लिए अनुमति दें, फिर दोबारा कोशिश करें।</span>'; b.after(n); });
  }
  function toggle() { current().then(function (sub) { return sub ? turnOff() : turnOn(); }); }

  function addButton(where) {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'pushb'; b.onclick = toggle;
    where.appendChild(b); buttons.push(b);
  }
  var foot = document.querySelector('.foot-write');
  if (foot) { var wrap = document.createElement('p'); foot.after(wrap); addButton(wrap); }
  current().then(function (sub) { paint(!!sub); if (sub) tellLang(); });
  new MutationObserver(function () { current().then(function (s) { if (s) tellLang(); }); }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-lang'] });

  // installed-app users: offer it once, a few seconds after opening
  if (standalone && !get('sd-push-asked') && Notification.permission === 'default') {
    setTimeout(function () {
      current().then(function (sub) {
        if (sub || document.querySelector('.ins')) return;
        var c = document.createElement('div'); c.className = 'push-card'; c.setAttribute('role', 'dialog');
        c.innerHTML = '<b><span class="en">A shloka a day, and festival reminders</span><span class="hi">रोज़ एक श्लोक, और पर्वों की याद</span></b><p><span class="en">One short notification each morning. Turn off any time.</span><span class="hi">हर सुबह एक छोटी सूचना। कभी भी बन्द करें।</span></p>';
        addButton(c);
        var no = document.createElement('button'); no.type = 'button'; no.className = 'no'; no.innerHTML = '<span class="en">Not now</span><span class="hi">अभी नहीं</span>';
        no.onclick = function () { c.remove(); set('sd-push-asked', '1'); }; c.appendChild(no);
        c.querySelector('.pushb').addEventListener('click', function () { setTimeout(function () { c.remove(); }, 1200); });
        document.body.appendChild(c); paint(false); set('sd-push-asked', '1');
      });
    }, 5000);
  }
})();
