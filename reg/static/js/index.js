$(document).ready(function() {

  if(!(/Android|iPhone|iPad|iPod|BlackBerry|Windows Phone/i).test(navigator.userAgent || navigator.vendor || window.opera)){
    skrollr.init({
      forceHeight: false
    });
  }

  var iOS = navigator.userAgent.match(/(iPod|iPhone|iPad)/);
  if(iOS){

    function iosVhHeightBug() {
      var height = $(window).height();
      $("header").css('min-height', height);
    }

    iosVhHeightBug();
    $(window).bind('resize', iosVhHeightBug);

  }

  $('#main')
    .transition('fade up in', 2000);

  $("#next").click(function() {
    $('html, body').animate({
      scrollTop: $("#info").offset().top
    }, 1000);
  });

  $('#c')
    .click(function(){
      location.href = '/6361746d6974'
    })

});

