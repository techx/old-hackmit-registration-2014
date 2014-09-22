$(document).ready(function() {
  var $form = $('.ui.form').not('.s3'),
      $resume = $('#resume'),
      $github =$('#github'),
      $mitHost = $('#mitHost'),
      $considerations = $('#considerations'),
      $address = $('#address');

 function showError(error){
    $form
      .removeClass('success')
      .addClass('error')
      .form('add errors', [
        error
      ])
  }

  $.fn.form.settings.rules.resume = function() {
    return $resume.hasClass('completed');
  };

  $.fn.form.settings.selector.group += ', .fields';

  $.fn.form.settings.rules.radio = function(value, id) {
    return $('#' + id).find('input[name=' + id + ']:checked').val() ? true: false
  };

  $form
    .form({
      resume: {
        identifier: 'resume',
        rules: [
          {
            type: 'resume',
            prompt: 'Please upload a PDF.'
          }
        ]
      },
      github: {
        identifier: 'github',
        rules: [
          {
            type: 'maxLength[39]',
            prompt: "Github usernames are 39 characters or fewer (their rules, not ours)."
          }
        ]
      },
     nonSmoking: {
        identifier: 'nonSmoking',
        rules: [
          {
            type: 'radio[nonSmoking]',
            prompt: "Please let us know if you need a non-smoking room or not."
          }
        ]
      },
      pets: {
        identifier: 'pets',
        rules: [
          {
            type: 'radio[pets]',
            prompt: "Please let us know if you're ok with pets in your room or not."
          }
        ]
      },
      mitHost: {
        identifier: 'mitHost',
        rules: [
          {
            type: 'maxLength[50]',
            prompt: "Please enter 50 or fewer characters for your MIT friend's name."
          }
        ]
      },
      considerations: {
        identifier: 'considerations',
        rules: [
          {
            type: 'maxLength[400]',
            prompt: "Please enter 400 or fewer characters for special hosting requests; email us about any more extensive concerns."
          }
        ]
      },
      address: {
        identifier: 'address',
        rules: [
          {
            type: 'empty',
            prompt: "Please enter your address so we can mail you a reimbursement check!"
          },
          {
            type: 'maxLength[150]',
            prompt: "Please enter 150 characters or fewer for your address; email us if your address is longer than that."
          }
        ]
      }
   },{
      onSuccess: submitConfirmation
    });

  function submitConfirmation() {

   function serializeRadio(id) {
     var radioValue = $('#' + id).find('input[name=' + id + ']:checked').val();
     if (typeof radioValue === 'undefined') {
       return null;
     } else {
       return radioValue === "yes" ? true : false
     }
   }

    var formData = JSON.stringify({
        resumeOptOut: false,
        resume: $resume.hasClass('completed'),
        github: $github.val(),
        mitHost: $mitHost.val(),
        nonSmoking: serializeRadio('nonSmoking'),
        pets: serializeRadio('pets'),
        considerations: $considerations.val(),
        address: $address.val()
      });

    var $dimmable = $('.ui.dimmable').dimmer('show');

    $.ajax({
      url:'/profiles',
      type: 'PUT',
      contentType:'application/json',
      dataType: 'json',
      data: formData,
      success: function(data){
        $dimmable.dimmer('hide');
        dimmerMessage(
          "Your profile update has been saved!",
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
});
 
