function throttle(fn, delay) {
    var last = void 0;
    var timer = void 0;

    return function () {
        var now = +new Date();

        if (last && now < last + delay) {
            clearTimeout(timer);

            timer = setTimeout(function () {
                last = now;
                fn ();
            }, delay);
        } else {
            last = now;
            fn ();
        }
    };
}


function onScroll () {
    if (window.pageYOffset) {
        $header.classList.add('is-active');
    } else {
        $header.classList.remove('is-active');
    }
}


var $header = document.querySelector('.js-header');

window.addEventListener('scroll', throttle(onScroll, 25));
