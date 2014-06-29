$(document).ready(function(){
  $('.lottery')
    .transition('fade in');

  $('.ui.dropdown')
    .dropdown();

  $('.ui.checkbox')
    .checkbox();

  var $form = $('.ui.form'),
      $name = $('#name'),
      $school = $('#school'),
      $gender = $('#gender'),
      $travelling = $('#travelling'),
      $adult = $('#adult'),
      $inviteCode = $('#invite');

  function submitLotteryApplication(){

    var formData = JSON.stringify({
        name: $name.val(),
        gender: $gender.val(),
        school: $school.val(),
        adult: $adult.val(),
        location: $travelling.val(),
        inviteCode: $inviteCode.val()
      });

    debugger;

    $.ajax({
      url:'/hackers',
      type: 'POST',
      contentType:'application/json',
      dataType: 'json',
      data: formData,
      success: function(data){
        $email.val("");
        $password.val("");
        $('.ui.page.dimmer')
          .dimmer('show');
      },
      error: function(error) {
        var msg = JSON.parse(error.responseText).message;
        showError(msg);
      }
    })
  }

  $form
    .form({
      name: {
        identifier: 'name',
        rules: [
          {
            type: 'empty',
            prompt: "Please enter your name!"
          }
        ]
      },
      gender: {
        identifier: 'gender',
        rules: [
          {
            type: 'empty',
            prompt: "Please select a gender!"
          }
        ]
      },
      school: {
        identifier: 'school',
        rules: [
          {
            type: 'empty',
            prompt: "Please enter your school name!"
          }
        ]
      },
      adult: {
        identifier: 'adult',
        rules: [
          {
            type: 'checked',
            prompt: "You must be 18 or older to participate!"
          }
        ]
      }
    },{
      onSuccess: submitLotteryApplication
    })

});