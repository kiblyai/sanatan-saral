// Offline support. Network first so a new version shows up straight away;
// the cache keeps the app playable with no internet.
const CACHE = 'hsm-v17';
const ASSETS = [
  './',
  'index.html',
  'manifest.json',
  'css/style.css',
  'js/app.js',
  'js/store.js',
  'js/i18n.js',
  'js/audio.js',
  'js/content.js',
  'js/chapters.js',
  'js/books.js',
  'js/talk.js',
  'js/util.js',
  'js/games/kit.js',
  'js/games/quiz.js',
  'js/games/build.js',
  'js/games/sort.js',
  'js/games/match.js',
  'js/games/meteor.js',
  'js/games/story.js',
  'js/games/spot.js',
  'js/games/order.js',
  'js/games/talk.js',
  'fonts/baloo2-devanagari.woff2',
  'fonts/baloo2-latin.woff2',
  'icons/icon.svg',
  'icons/icon-192.png',
  'icons/icon-512.png',
];

self.addEventListener('install', (event) => {
  // cache: 'reload' skips the browser's HTTP cache, so a new version never stores old files.
  const fresh = ASSETS.map((url) => new Request(url, { cache: 'reload' }));
  event.waitUntil(caches.open(CACHE).then((c) => c.addAll(fresh)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== self.location.origin) return;
  event.respondWith(
    // no-cache: always ask the server whether the file changed before using a stored copy.
    fetch(req.url, { cache: 'no-cache', credentials: 'same-origin' })
      .then((res) => {
        if (res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
        }
        return res;
      })
      .catch(() => caches.match(req, { ignoreSearch: true }).then((hit) => hit || caches.match('index.html'))),
  );
});
