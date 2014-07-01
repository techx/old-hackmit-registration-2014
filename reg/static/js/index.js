$(document).ready(function() {

  skrollr.init({
    forceHeight: false
  });

  $('#main')
    .transition('fade up in', 2000);

  $("#next").click(function() {
    $('html, body').animate({
      scrollTop: $("#info").offset().top
    }, 1000);
  });

});
