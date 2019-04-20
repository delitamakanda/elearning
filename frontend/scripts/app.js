'use strict';

$(function() {
    // navbar dropdown
    var $navbarBurgers = $('body').find('.navbar-burger');

    if ($navbarBurgers.length > 0) {
        $navbarBurgers.each(function(i){
            $(this).on('click', function(e) {
                e.preventDefault();

                var target = $(this).data('target'),
                    $target = $('#sidebar');

                $(this).toggleClass('is-active');
                $target.toggleClass('is-active');
            });
        });
    }
});
