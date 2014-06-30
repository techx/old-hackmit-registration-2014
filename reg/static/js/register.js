$(document).ready(function() {

  var $form     = $('.ui.form'),
      $email    = $('#email'),
      $password = $('#password');

  function register(){

    if (!$email.val().match(/.edu/gi)){
      showError('Please use a .edu email.');
      return;
    }

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
        var dimmer = $('.ui.page.dimmer')
          .dimmer('show');
        setTimeout(function(){
          dimmer.dimmer('hide')
        }, 3000)
      },
      error: function(error) {
        var msg = JSON.parse(error.responseText).message;
        showError(msg);
      }
    })
  }

  $(".register")
    .transition('fade up in');

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