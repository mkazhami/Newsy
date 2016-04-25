//application.js

$(document).ready(function() {
	$(".nav a").click(function() {
		const id = $(this).attr('id');
    $('html, body').stop().animate({
      scrollTop: $("." + id).offset().top - 60
    }, 1000);
	});
});