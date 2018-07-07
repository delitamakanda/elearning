var cacheName = 'v4';
var cacheFiles = [
    './static/fonts/custom/custom.eot',
    './static/fonts/custom/custom.ttf',
    './static/fonts/custom/custom.woff',
	'./static/scripts/offline.js',
	'./static/styles/fonts.css',
	'./static/styles/main.css'
];

self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open(cacheName).then(function(cache) {
            console.log('[ServiceWorker] Caching cacheFiles');
            return cache.addAll(cacheFiles);
        })
	);
});

self.addEventListener('activate', function(e) {
    e.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(cacheNames.map(function(thisCacheName) {
                if (thisCacheName !== cacheName) {

                    console.log('[ServiceWorker] Removing Cached Files from Cache - ', thisCacheName);
                    return caches.delete(thisCacheName);
                }
            }));
        })
	);
});

self.addEventListener('fetch', (event) => {
    event.respondWith(

		caches.match(event.request).then((response) => {
        	if ( response ) return response
			return fetch(event.request)
		})
    );
});
