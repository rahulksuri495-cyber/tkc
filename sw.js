/* TKC Talent service worker — offline app shell */
const VERSION = 'tkc-v6';
const STATIC_CACHE = `${VERSION}-static`;
const RUNTIME_CACHE = `${VERSION}-runtime`;
const OFFLINE_URL = '/offline.html';

const PRECACHE = [
  '/offline.html',
  '/manifest.webmanifest',
  '/apple-touch-icon.png',
  '/icon-192.png',
  '/icon-512.png',
];

function isCacheableResponse(response) {
  if (!response || !response.ok || response.status !== 200) return false;
  return response.type === 'basic' || response.type === 'cors';
}

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) =>
      Promise.allSettled(PRECACHE.map((u) => cache.add(u)))
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((k) => k !== STATIC_CACHE && k !== RUNTIME_CACHE)
          .map((k) => caches.delete(k))
      )
    ).then(() => self.clients.claim())
  );
});

function isHashedAsset(url) {
  // Vite-style hashed assets: /assets/name-HASH.ext
  return /\/assets\/.+-[A-Za-z0-9_-]{8,}\.[a-z0-9]+$/i.test(url.pathname);
}

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  // Navigation requests → NetworkFirst, fall back to cache, then offline page
  if (req.mode === 'navigate') {
    event.respondWith(
      (async () => {
        try {
          const fresh = await fetch(req);
          // Never persist temporary firewall/challenge responses. A cached 403
          // can otherwise leave this route blank even after the challenge passes.
          if (isCacheableResponse(fresh)) {
            const contentType = fresh.headers.get('content-type') || '';
            if (contentType.includes('text/html')) {
              const cache = await caches.open(RUNTIME_CACHE);
              await cache.put(req, fresh.clone());
            }
          }
          return fresh;
        } catch (_) {
          const cached = await caches.match(req);
          if (cached) return cached;
          const home = await caches.match('/');
          if (home) return home;
          return caches.match(OFFLINE_URL);
        }
      })()
    );
    return;
  }

  // Hashed static assets → CacheFirst (immutable)
  if (isHashedAsset(url)) {
    event.respondWith(
      caches.match(req).then((hit) =>
        hit ||
        fetch(req).then((res) => {
          if (isCacheableResponse(res)) {
            const copy = res.clone();
            caches.open(STATIC_CACHE).then((c) => c.put(req, copy));
          }
          return res;
        })
      )
    );
    return;
  }

  // Images / CSS / JS / fonts → StaleWhileRevalidate
  if (/\.(?:css|js|png|jpg|jpeg|webp|svg|gif|ico|woff2?|ttf|otf)$/i.test(url.pathname)) {
    event.respondWith(
      caches.match(req).then((cached) => {
        const network = fetch(req)
          .then((res) => {
              if (isCacheableResponse(res)) {
                const copy = res.clone();
                caches.open(RUNTIME_CACHE).then((c) => c.put(req, copy));
              }
            return res;
          })
          .catch(() => cached);
        return cached || network;
      })
    );
  }
});