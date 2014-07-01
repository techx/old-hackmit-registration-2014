$(document).ready(function() {

  var $form     = $('.ui.form'),
      $email    = $('#email'),
      $password = $('#password');

  function login(){

    var $dimmable = $('.ui.dimmable').dimmer('show');

    $.ajax({
      url:'/sessions',
      type: 'POST',
      contentType:'application/json',
      dataType: 'json',
      data: JSON.stringify({
        type: 'hacker',
        email: $email.val(),
        hashedPassword: SHA224($password.val())
      }),
      success: function(data){
        $dimmable.dimmer('hide');
        if (data.url){
          location.href = data.url
        }
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
      onSuccess: login
    })

});