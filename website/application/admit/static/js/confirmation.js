$(document).ready(function(){
  var $form = $('.ui.form').not('.s3'),
      $badge = $('#badge'),
      $phone = $('#phone'),
      $shirt = $('#shirt'),
      $diet = $('#diet'),
      $waiver = $('#waiver'),
      $photoRelease = $('#photoRelease');
      $resumeOptOut = $('#resumeOptOut');
      $resume = $('.s3.upload.form').eq(0).find('div[class*=s3][class*=upload][class*=button]');
      $travel = $('.s3.upload.form').eq(1).find('div[class*=s3][class*=upload][class*=button]');

  $resumeOptOut.prop('checked', $resumeOptOut.val() === "True");
  $resumeOptOut.click(function() { console.log('clicked'); } );

  function validate() {
    console.log($resume.hasClass('completed'));
    console.log($('[name=likelihood]:checked') === [])
    debugger;
    submitConfirmation();
  }
  
  function submitConfirmation() {

    var formData = JSON.stringify({
        badge: $badge.val(),
        phone: $phone.val().replace(/[^0-9]/gi, ""),
        shirt: $shirt.val(),
        diet: $diet.val(),
        waiver: $waiver.val(),
        photoRelease: $photoRelease.val(),
        resumeOptOut: $resumeOptOut.is(':checked'),
        resume: $resume.hasClass('completed'),
        travel: $travel.hasClass('completed')
      });

    var $dimmable = $('.ui.dimmable').dimmer('show');

    $.ajax({
      url:'/admits',
      type: 'PUT',
      contentType:'application/json',
      dataType: 'json',
      data: formData,
      success: function(data){
        $dimmable.dimmer('hide');
        dimmerMessage(
          "Your confirmation has been saved!",
          "And now we wait...",
          function(){
            location.href="/dashboard"
          }, 1500
        );
      },
      error: function(error) {
        $dimmable.dimmer('hide');
        var msg = JSON.parse(error.responseText).message;
        showError(msg);
      }
    })
  }

  function showError(error){
    $form
      .removeClass('success')
      .addClass('error')
      .form('add errors', [
        error
      ])
  }

  $.fn.form.settings.rules.phone = function(val){
    if (!/[^0-9]/gi.test(val)){
      var stripped = val.replace(/[^0-9]/gi, "");
      return stripped.length >= 10 && stripped.length <= 15
    }
    return false
  };

  $form
    .form({
      name: {
        identifier: 'badge',
        rules: [
          {
            type: 'empty',
            prompt: "Please enter the name you wanted printed on your badge!"
          }
        ]
      },
      phone: {
        identifier: 'phone',
        rules: [
          {
            type: 'empty',
            prompt: 'Please enter your phone number.'
          },{
            type: 'phone',
            prompt: 'Please enter a valid phone number.'
          }

        ]
      },
      shirt: {
        identifier: 'shirt',
        rules: [
          {
            type: 'empty',
            prompt: "Please pick a t-shirt size!"
          }
        ]
      },
      diet: {
        identifier: 'diet',
        rules: [
          {
            type: 'empty',
            prompt: "Please pick a dietary restriction! If you don't have any, just choose None."
          }
        ]
      },
      waiver: {
        identifier: 'waiver',
        rules: [
          {
            type: 'empty',
            prompt: "Please enter your full legal name."
          }
        ]
      },
      photoRelease: {
        identifier: 'photoRelease',
        rules: [
          {
            type: 'empty',
            prompt: 'Please enter your full legal name.'
          }
        ]
      }
    },{
      onSuccess: validate
    })

});
