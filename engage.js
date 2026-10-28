/* Every page: a "Share" pill in the top bar, and at the end "Share this page" + "Was this helpful?" (public site only). */
(function () {
  var hi = function () { return document.documentElement.getAttribute('data-lang') === 'hi'; };
  var ev = function (n, p) { try { gtag('event', n, p || {}); } catch (e) {} };
  var page = location.pathname.replace(/^\//, '') || 'index.html';
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function h1(lang) { var h = document.querySelector('h1'); if (!h) return document.title; var s = h.querySelector('.' + lang); return (s || h).textContent.replace(/\s+/g, ' ').trim(); }
  function url(src) { var u = new URL(location.href); u.hash = ''; ['utm_source', 'utm_medium', 'utm_campaign'].forEach(function (k) { u.searchParams.delete(k); }); u.searchParams.set('utm_source', src); u.searchParams.set('utm_medium', 'share'); return u.toString(); }
  function msg(src) { return hi() ? ('📖 ' + h1('hi') + ' — सरल हिन्दी और अंग्रेज़ी में, निःशुल्क:\n' + url(src)) : ('📖 ' + h1('en') + ' — in simple English and Hindi, free:\n' + url(src)); }
  function share(where) {
    ev('share_page', { method: navigator.share ? 'native' : 'whatsapp', where: where });
    if (navigator.share) { navigator.share({ title: document.title, text: msg('share') }).catch(function () {}); }
    else { window.open('https://wa.me/?text=' + encodeURIComponent(msg('whatsapp')), '_blank', 'noopener'); }
  }
  var WA = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7.5-.1 1.5-.6 1.8-1.2s.2-1.1.1-1.2l-.4-.2z"/></svg>';

  var st = document.createElement('style');
  st.textContent = '.sp-btn{flex-shrink:0;display:inline-flex;align-items:center;gap:.35rem;font:inherit;font-size:.92rem;color:var(--ink,#20363A);background:var(--paper,#fff);border:1.5px solid var(--line,#ccd);border-radius:99px;padding:.26rem .7rem;cursor:pointer;white-space:nowrap}' +
    '.sp-btn:hover{border-color:var(--indigo,#3C6C72)}@media (max-width:560px){.sp-btn .sl{display:none}.sp-btn{padding:.3rem .5rem;order:3}}' +
    '.pe{max-width:var(--measure,760px);margin:2.4rem auto 1rem;padding:1.1rem 1.2rem;border:1.5px solid var(--line,#D5E0DA);border-radius:18px;background:var(--paper,#fff);display:grid;gap:1rem}' +
    '.pe-row{display:flex;flex-wrap:wrap;align-items:center;gap:.6rem .8rem}.pe b{font-size:1.02rem}' +
    '.pe button{font:inherit;font-weight:700;min-height:44px;border-radius:99px;padding:.45rem 1rem;cursor:pointer;display:inline-flex;align-items:center;gap:.4rem}' +
    '.pe .pe-wa{background:#1f8f4e;color:#fff;border:0}.pe .pe-copy,.pe .pe-fb{background:var(--paper,#fff);color:var(--ink,#20363A);border:1.5px solid var(--line,#ccd)}' +
    '.pe .pe-fb[aria-pressed="true"]{border-color:var(--indigo,#3C6C72);background:color-mix(in srgb,var(--indigo,#3C6C72) 10%,var(--paper,#fff))}' +
    '.pe-thanks{color:var(--ink-2,#566B6D);font-size:.95rem}@media print{.sp-btn,.pe{display:none!important}}';
  document.head.appendChild(st);

  function L(en, h) { return '<span class="en">' + en + '</span><span class="hi">' + h + '</span>'; }

  // top bar pill, next to Print
  function addPill() {
    var bar = document.querySelector('.bar'); if (!bar || bar.querySelector('.sp-btn')) return;
    var b = document.createElement('button'); b.type = 'button'; b.className = 'sp-btn'; b.setAttribute('aria-label', 'Share this page');
    b.innerHTML = WA + '<span class="sl">' + L('Share', 'भेजें') + '</span>';
    b.addEventListener('click', function () { share('top'); });
    var pr = bar.querySelector('.print-btn'); if (pr) pr.parentNode.insertBefore(b, pr.nextSibling); else bar.appendChild(b);
  }

  // end-of-page block
  var box = document.createElement('section'); box.className = 'pe'; box.setAttribute('aria-label', 'Share and feedback');
  var done = get('fb:' + page);
  box.innerHTML =
    '<div class="pe-row"><b>' + L('Found this useful? Share it with a family.', 'उपयोगी लगा? किसी परिवार को भेजें।') + '</b>' +
    '<button type="button" class="pe-wa">' + WA + L('Share on WhatsApp', 'WhatsApp पर भेजें') + '</button>' +
    '<button type="button" class="pe-copy">' + L('Copy link', 'लिंक कॉपी करें') + '</button></div>' +
    '<div class="pe-row"><b>' + L('Was this page helpful?', 'क्या यह पृष्ठ उपयोगी था?') + '</b>' +
    '<button type="button" class="pe-fb" data-v="yes" aria-pressed="' + (done === 'yes') + '">👍 ' + L('Yes', 'हाँ') + '</button>' +
    '<button type="button" class="pe-fb" data-v="no" aria-pressed="' + (done === 'no') + '">👎 ' + L('Not really', 'ज़्यादा नहीं') + '</button>' +
    '<span class="pe-thanks" aria-live="polite"></span></div>';
  box.querySelector('.pe-wa').addEventListener('click', function () {
    ev('share_page', { method: 'whatsapp', where: 'end' });
    window.open('https://wa.me/?text=' + encodeURIComponent(msg('whatsapp')), '_blank', 'noopener');
  });
  box.querySelector('.pe-copy').addEventListener('click', function () {
    var b = this, u = url('copy'), ok = function () { b.innerHTML = L('Copied ✓', 'कॉपी हो गया ✓'); }; ev('share_page', { method: 'copy', where: 'end' });
    if (navigator.clipboard) navigator.clipboard.writeText(u).then(ok, function () { prompt('Copy', u); }); else prompt('Copy', u);
  });
  var thanks = box.querySelector('.pe-thanks');
  box.querySelectorAll('.pe-fb').forEach(function (b) {
    b.addEventListener('click', function () {
      var v = b.getAttribute('data-v');
      box.querySelectorAll('.pe-fb').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      if (get('fb:' + page) !== v) { ev('page_feedback', { helpful: v, page_path: '/' + page }); set('fb:' + page, v); }
      thanks.innerHTML = v === 'yes' ? L('Thank you! 🙏', 'धन्यवाद! 🙏') : L('Thanks. <a href="contact.html?topic=suggestion&ref=' + encodeURIComponent(page) + '">Tell us what was missing</a>', 'धन्यवाद। <a href="contact.html?topic=suggestion&ref=' + encodeURIComponent(page) + '">बताइए क्या कमी थी</a>');
    });
  });
  function place() {
    var f = document.querySelector('footer');
    if (f && f.parentNode) f.parentNode.insertBefore(box, f); else (document.querySelector('main') || document.body).appendChild(box);
    addPill(); setTimeout(addPill, 800);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', place); else place();
})();
