$(document).ready(function(){

  var $form = $('.ui.form'),
      $token = $('#token'),
      $newPassword = $('#password'),
      $dimmable = $('.ui.dimmable');

  function forgot(){

    $dimmable.dimmer('show');

    $.ajax({
      url:'/accounts/reset?token=' + $token.val(),
      type: 'POST',
      contentType:'application/json',
      dataType: 'json',
      data: JSON.stringify({
        newPassword: SHA224($newPassword.val())
      }),
      success: function(data){
        $dimmable.dimmer('hide');
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

  function showError(msg){
    $dimmable.dimmer('hide');
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
