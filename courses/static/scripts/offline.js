var isOffline = false;
window.addEventListener('load', checkConnectivity);

function checkConnectivity() {
    updateStatus();
    window.addEventListener('online', updateStatus);
    window.addEventListener('offline', updateStatus);
}

function updateStatus() {
    if (typeof navigator.onLine !== 'undefined') {
        isOffline = !navigator.onLine;
        document.documentElement.classList.toggle('is-offline', isOffline);
    }
    var notification = document.querySelector('#notification');
    if (isOffline) {
        notification.textContent = "You appear to be offline ";
        notification.removeAttribute('hidden');
    } else {
        notification.textContent = "";
        notification.removeAttribute('hidden');
    }
}

var links = document.querySelectorAll('a[href]');

Array.from(links).forEach((link) => {
    caches.match(link.href, { ignoreSearch: true }).then((response) => {
        if (response) {
            link.classList.add('is-cached');
        }
    });
});
