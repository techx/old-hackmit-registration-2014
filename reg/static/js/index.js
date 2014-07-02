$(document).ready(function() {

  if(!(/Android|iPhone|iPad|iPod|BlackBerry|Windows Phone/i).test(navigator.userAgent || navigator.vendor || window.opera)){
    skrollr.init({
      forceHeight: false
    });
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

  var viewportUnitsBuggyfill = require('viewport-units-buggyfill');

  // find viewport-unit declarations,
  // convert them to pixels,
  // inject style-element into document,
  // register orientationchange event to repeat when necessary
  // will only engage for Mobile Safari on iOS
  viewportUnitsBuggyfill.init();
  // ignore user agent force initialization
  viewportUnitsBuggyfill.init(true);

  // update internal declarations cache and recalculate pixel styles
  // this is handy when you add styles after .init() was run
  viewportUnitsBuggyfill.refresh();

  // you can do things manually (without the style-element injection):
  // identify all declarations using viewport units
  viewportUnitsBuggyfill.findProperties();
  var cssText = viewportUnitsBuggyfill.getCss();
});
