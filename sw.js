/* Offline support: pages you open are saved so they work without internet. Version 20261030075310. */
const V = 'saral-20261030075310';
const CORE = ["/", "/style.css", "/lang.js", "/share.js", "/interactive.js", "/verse-tools.js", "/manifest.webmanifest", "/icon-192.png"];
self.addEventListener('install', e => { e.waitUntil(caches.open(V).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V && !k.startsWith('sd-')).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const r = e.request;
  if (r.method !== 'GET') return;
  const u = new URL(r.url);
  const same = u.origin === location.origin;
  const fonts = /fonts\.(googleapis|gstatic)\.com$/.test(u.hostname);
  if (!same && !fonts) return;
  if (/\.(mp4|webm)$/.test(u.pathname)) return;
  if (r.mode === 'navigate' || (same && u.pathname.endsWith('.html'))) {
    e.respondWith(fetch(r).then(res => { const c = res.clone(); caches.open(V).then(x => x.put(r, c)); return res; })
      .catch(() => caches.match(r, {ignoreSearch: true}).then(m => m || caches.match('/'))));
    return;
  }
  e.respondWith(caches.match(r).then(m => {
    const net = fetch(r).then(res => { if (res.ok || res.type === 'opaque') { const c = res.clone(); caches.open(V).then(x => x.put(r, c)); } return res; }).catch(() => m);
    return m || net;
  }));
});

// ---- notifications: the push carries no text; we show today's entry from /push/<month>.json ----
async function getLang() { try { const r = await (await caches.open('sd-prefs')).match('/__lang'); return r ? await r.text() : 'en'; } catch (e) { return 'en'; } }
self.addEventListener('message', e => { if (e.data && e.data.type === 'lang') e.waitUntil(caches.open('sd-prefs').then(c => c.put('/__lang', new Response(e.data.lang === 'hi' ? 'hi' : 'en')))); });
self.addEventListener('push', e => { e.waitUntil((async () => {
  const lang = await getLang(), d = new Date(), key = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  let item = null;
  try { const feed = await (await fetch('/push/' + key.slice(0, 7) + '.json', {cache: 'no-store'})).json(); item = feed[key]; } catch (err) {}
  if (!item) item = {t_en: 'Today’s shloka', t_hi: 'आज का श्लोक', b_en: 'A verse a day, explained simply.', b_hi: 'हर दिन एक श्लोक, सरल भाषा में।', url: '/?utm_source=push'};
  const hi = lang === 'hi';
  await self.registration.showNotification(hi ? item.t_hi : item.t_en, { body: hi ? item.b_hi : item.b_en, icon: '/icon-192.png', badge: '/icon-192.png', tag: 'daily', data: {url: item.url} });
})()); });
self.addEventListener('notificationclick', e => { e.notification.close(); const u = (e.notification.data && e.notification.data.url) || '/'; e.waitUntil(clients.openWindow(u)); });
