$(document).ready(function(){
  var $form = $('.ui.form').not('.s3'),
      $badge = $('#badge'),
      $phone = $('#phone'),
      $shirt = $('#shirt'),
      $graduation = $('#graduation'),
      $meng = $('#meng'),
      $diet = $('#diet'),
      $waiver = $('#waiver'),
      $photoRelease = $('#photoRelease'),
      $resumeOptOut = $('#resumeOptOut'),
      $resume = $('.s3.upload.form').eq(0).find('div[class*=s3][class*=upload][class*=button]'),
      $github =$('#github'),
      $travel = $('.s3.upload.form').eq(1).find('div[class*=s3][class*=upload][class*=button]');

  $resumeOptOut.prop('checked', $resumeOptOut.val() === "True");

  function submitConfirmation() {

    var formData = JSON.stringify({
        badge: $badge.val(),
        phone: $phone.val().replace(/[^0-9]/gi, ""),
        shirt: $shirt.val(),
        graduation: $graduation.val(),
        meng: $meng.is(':checked'),
        diet: $diet.val(),
        waiver: $waiver.val(),
        photoRelease: $photoRelease.val(),
        resumeOptOut: $resumeOptOut.is(':checked'),
        resume: $resume.hasClass('completed'),
        github: $github.val(),
        travel: $travel.hasClass('completed'),
        likelihood: $('input[name=likelihood]:checked', '#likelihood').val()
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
    var stripped = val.replace(/[^0-9]/gi, "");
    return stripped.length >= 10 && stripped.length <= 15
  };

  $.fn.form.settings.rules.likelihood = function(){
    return $('input[name=likelihood]:checked', '#likelihood').val() ? true: false
  };

  $.fn.form.settings.rules.optOut = function(){
    return $resumeOptOut.is(':checked') ^ $resume.hasClass('completed')
  };

  $.fn.form.settings.rules.travel = function(){
    return $travel.hasClass('completed')
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
      graduation: {
        identifier: 'graduation',
        rules: [
          {
            type: 'empty',
            prompt: "Please pick a graduation year! You can't stay in school forever."
          }
        ]
      },
      diet: {
        identifier: 'diet',
        rules: [
          {
            type: 'empty',
            prompt: "Please pick a dietary restriction! If you don't have any, just choose 'No restrictions'."
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
      travel {
        identifier: 'travel',
        rules: [
          {
            type: 'empty',
            prompt: "You must upload a travel receipt to confirm your spot."
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
      },
      resume: {
        identifier: 'resumeOptOut',
        rules: [
          {
            type: 'optOut',
            prompt: 'Please upload a PDF!'
          }
        ]
      },
      likelihood: {
        identifier: 'likelihood',
        rules: [
          {
            type: 'likelihood',
            prompt: 'Please choose how likely you are to come!'
          }
        ]
      }
    },{
      onSuccess: submitConfirmation
    })
});

