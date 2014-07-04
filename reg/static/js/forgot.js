$(document).ready(function(){

  var $form = $('.ui.form'),
      $email= $('#email'),
      $token = $('#token'),
      $newPassword = $('#password');

  function forgot(){

    debugger;

    if($token.val()){
      $.ajax({
        url:'/accounts/reset?token=' + $token.val(),
        type: 'POST',
        contentType:'application/json',
        dataType: 'json',
        data: JSON.stringify({
          newPassword: SHA224($newPassword.val())
        }),
        success: function(data){
          dimmerMessage(
            data.message,
            "",
            function(){
              location.href= "/dashboard"
            }, 1500
          );
        },
        error: showError
      })
    } else {
      $.ajax({
        url:'/forgot',
        type: 'POST',
        contentType:'application/json',
        dataType: 'json',
        data: JSON.stringify({
          email: $email.val()
        }),
        success: function(data){
          dimmerMessage(
            data.message,
            "",
            function(){
              location.href= "/dashboard"
            }, 1500
          );
        },
        error: showError
      })
    }
  }

  function showError(msg){

    var error = JSON.parse(msg.responseText).message;
    $form
      .removeClass('success')
      .addClass('error')
      .form('add errors',[
        error
      ]);
    $email.addClass('error');
  }

  $form
    .form({
      email: {
        identifier: 'email',
        rules: [
          {
            type: 'email',
            prompt: "That's not a valid email!"
          },
          {
            type: 'empty',
            prompt: 'Please enter a new password!'
          }
        ]
      },
      password: {
        identifier: 'password',
        rules: [
          {
            type: 'empty',
            prompt: 'Please enter a password!'
          }
        ]
      },
      confirm: {
        identifier: 'confirm',
        rules: [
          {
            type: 'match[password]',
            prompt: "Whoops, your passwords don't match!"
          }
        ]
      }
    },{
      onSuccess: forgot
    })

});
