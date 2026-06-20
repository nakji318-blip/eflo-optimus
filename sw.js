const CACHE_NAME = 'eflo-optimus-v2';
const ASSETS = [
  '/',
  '/index.html',
  '/eflo_field_ai_bot.html',
  '/eflo_onboarding_v2.html',
  '/intex_pod.html',
  '/ss_pod.html',
  '/manifest_top.json',
  '/manifest_bot.json',
  '/manifest_school.json',
  '/manifest_intex.json',
  '/manifest_ss.json',
  '/icon_bot.png',
  '/icon_school.png',
  '/icon_intex.png',
  '/icon_ss.png'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return Promise.all(
        ASSETS.map(url =>
          cache.add(url).catch(err => console.warn('キャッシュ失敗(無視):', url, err))
        )
      );
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  if (e.request.url.includes('/api/claude') || e.request.url.includes('api.anthropic.com')) {
    e.respondWith(fetch(e.request));
    return;
  }
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(res => {
        if (res.ok) {
          const resClone = res.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(e.request, resClone));
        }
        return res;
      }).catch(() => cached);
    })
  );
});
