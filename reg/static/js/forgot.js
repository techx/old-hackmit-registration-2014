$(document).ready(function(){

  var $form = $('.ui.form'),
      $email= $('#email');

  function forgot(){

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
      error: function(error) {
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
            prompt: "You gotta give me something, here."
          }
        ]
      }
    },{
      onSuccess: forgot
    })

});
