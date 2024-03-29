$(document).ready(function(){

  var $form = $('.ui.form'),
      $id   = $('#id'),
      $email= $('#email'),
      $old  = $('#oldPassword'),
      $new  = $('#newPassword');

  function reset(){

    var $dimmable = $('.ui.dimmable').dimmer('show');
    $.ajax({
      url:'/accounts/' + $id.val(),
      type: 'PUT',
      contentType:'application/json',
      dataType: 'json',
      data: JSON.stringify({
        email: $email.val(),
        oldPassword: SHA224($old.val()),
        newPassword: SHA224($new.val())
      }),
      success: function(data){
        $dimmable.dimmer('hide');
        dimmerMessage(
          data.message,
          "",
          function(){
            location.href= "/logout"
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

  function showError(error){
    $form
      .removeClass('success')
      .addClass('error')
      .form('add errors',[
        error
      ])
      .children('.old.password.field')
        .addClass('error');
    $old.val("");
    $new.val("");
    $confirm.val("");
  }

  $form
    .form({
      old: {
        identifier: 'oldPassword',
        rules: [
          {
            type: 'empty',
            prompt: 'Please enter your old password!'
          }
        ]
      },
      new: {
        identifier: 'newPassword',
        rules: [
          {
            type: 'empty',
            prompt: 'Please enter a new password!'
          }
        ]
      },
      confirm: {
        identifier: 'confirm',
        rules: [
          {
            type: 'match[newPassword]',
            prompt: "Whoops, your passwords don't match!"
          }
        ]
      }
    },{
      onSuccess: reset
    })

});
