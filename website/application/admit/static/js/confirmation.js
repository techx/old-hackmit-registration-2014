$(document).ready(function(){
  var $form = $('.ui.form'),
      $badge = $('#badge'),
      $phone = $('#phone'),
      $shirt = $('#shirt'),
      $diet = $('#diet'),

  $diet.change(function(){
    if ("other" === $diet.val()){
      // TODO: pop up a message saying we'll give you a gift card at the event
    }
  });

  function validate(){

    submitConfirmation();
  }
  
  function submitConfirmation(){

    var formData = JSON.stringify({
        badge: $badge.val(),
        phone: $phone.val(),
        shirt: $shirt.val(),
        diet: $diet.val(),
      });

    var $dimmable = $('.ui.dimmable').dimmer('show');

    $.ajax({
      url:'/admits',
      type: 'PUT',
      contentType:'application/json',
      dataType: 'json',
      data: formData,
      success: function(data){
        $dimmable.dimmer('hide');
        dimmerMessage(
          "Your confirmation has been saved!",
          "And now we wait...",
          function(){
            location.href="/dashboard"
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
      .form('add errors', [
        error
      ])
  }

  $form
    .form({
      name: {
        identifier: 'badge',
        rules: [
          {
            type: 'empty',
            prompt: "Please enter the name you wanted printed on your badge!"
          }
        ]
      },
      diet: {
        identifier: 'diet',
        rules: [
          {
            type: 'empty',
            prompt: "Please enter a dietary restriction!"
          }
        ]
      }
    },{
      onSuccess: validate
    })

});
