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

                $target.toggleClass('is-active');
            });
        });
    }

    // flash message
    var $flashMessage = $('.alert');
	if ($flashMessage.length === 0) {
		return;
	}

	var FLASH_MESSAGE_DELAY_BEFORE_HIDE = 8000;

	// Declare
	var hideOne = function ($flashMessage) {
		$flashMessage.slideUp(function () {
			$(this).detach();
		});
	};

	var launchTimer = function () {
		window.timerFlashMessage = setTimeout(function () {
			$flashMessage.each(function () {
				hideOne($(this));
			});
		}, FLASH_MESSAGE_DELAY_BEFORE_HIDE);
	};

	// Init
	var $closeButton = $flashMessage.find('.close');

	if ($flashMessage.data('is-auto-close')) {
		launchTimer();
	}

	// Events
	$closeButton.on('click', function () {
		hideOne($(this).parents('.alert'));
	});
});
