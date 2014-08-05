$(document).ready(function() {

  var $form     = $('.ui.form'),
      $email    = $('#email'),
      $password = $('#password'),
      $confirm  = $('#confirm');

  function register(){

    var $dimmable = $('.ui.dimmable').dimmer('show');

    $.ajax({
      url:'/accounts',
      type: 'POST',
      contentType:'application/json',
      dataType: 'json',
      data: JSON.stringify({
        role: 'hacker',
        email: $email.val(),
        hashedPassword: SHA224($password.val())
      }),
      success: function(data){
        $email.val("");
        $password.val("");
        $confirm.val("");

        $dimmable.dimmer('hide');

        dimmerMessage(
          "You're not done yet! Check your email for verification.",
          "Then, complete your registration to enter the lottery.",
          function(){
            location.href= "/login"
          }, 3000
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
      .form('add errors',[
        error
      ])
      .children('.email.field')
        .addClass('error');
    $password.val("");
    $confirm.val("");
  }

  // ONLY FOR USC TEMPORARILY, TODO: REMOVE
  $.fn.form.settings.rules.usc = function(value){
    return !value.match("usc.edu$")
  };

  $form
    .form({
      email: {
        identifier: 'email',
        rules: [
          {
            type: 'usc', // ONLY FOR USC TEMPORARILY, TODO: REMOVE
            prompt: "Issues have been reported with using usc.edu emails. We suggest you try another email (ex. gmail) instead!"
          },
          {
            type: 'empty',
            prompt: "Please enter an email!"
          },
          {
            type: 'email',
            prompt: "That's not a valid email address :("
          }

        ]
      },
      password: {
        identifier: 'password',
        rules: [
          {
            type: 'empty',
            prompt: "Please enter a password!"
          }
        ]
      },
      confirm: {
        identifier: 'confirm',
        rules: [
          {
            type: 'match[password]',
            prompt: "Your passwords don't match!"
          }
        ]
      }

    },{
      onSuccess: register
    })
});
