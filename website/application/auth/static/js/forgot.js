$(document).ready(function(){

  var $form = $('.ui.form'),
      $email= $('#email'),
      $dimmable = $('.ui.dimmable');

  function forgot(){

    $dimmable.dimmer('show');

    $.ajax({
      url:'/forgot',
      type: 'POST',
      contentType:'application/json',
      dataType: 'json',
      data: JSON.stringify({
        email: $email.val()
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
      }
    },{
      onSuccess: forgot
    })

});
