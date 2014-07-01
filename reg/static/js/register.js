$(document).ready(function() {

  var $form     = $('.ui.form'),
      $email    = $('#email'),
      $password = $('#password');

  function register(){

    if (!$email.val().match(/.edu/gi)){
      showError('Please use a .edu email.');
      return;
    }

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

        $dimmable.dimmer('hide');

        dimmerMessage(
          "Thanks for registering!",
          "Check your email for verification.",
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
  }

  $form
    .form({
      email: {
        identifier: 'email',
        rules: [
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
      }
    },{
      onSuccess: register
    })


});