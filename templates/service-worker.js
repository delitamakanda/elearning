var cacheName = 'v5';
var cacheFiles = [];
var CURRENT_CACHES = {
    offline: 'offline-v1'
};

var OFFLINE_URL = '/offline.html';

self.addEventListener('install', function(e) {
    e.waitUntil(
        fetch(createCacheBustedRequest(OFFLINE_URL)).then(function(response) {
            return caches.open(CURRENT_CACHES.offline).then(function(cache) {
                console.log('[ServiceWorker] Caching cacheFiles');
                return cache.put(OFFLINE_URL, response);
            })
        })
    )

    function createCacheBustedRequest(url) {
        var request = new Request(url, {cache: 'reload'});
        if ('cache' in request) {
            return request;
        }
        var bustedUrl = new URL(url, self.location.href);
        bustedUrl.search += (bustedUrl.search ? '&' : '') + 'cachebust=' + Date.now();
        return new Request(bustedUrl);
    }
});

self.addEventListener('activate', function(e) {
    var expectedCacheNames = Object.keys(CURRENT_CACHES).map(function(key) {
        return CURRENT_CACHES[key];
    });

    e.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (expectedCacheNames.indexOf(cacheName) === -1) {

                        console.log('[ServiceWorker] Removing Cached Files from Cache - ', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
	);
});

self.addEventListener('fetch', function(event) {
    if (event.request.mode === 'navigate' ||
        (event.request.method === 'GET' &&
        event.request.headers.get('accept').includes('text/html'))) {

        event.respondWith(
            fetch(event.request).catch(function(error) {
                return caches.match(OFFLINE_URL);
            })
        )
    }
});
