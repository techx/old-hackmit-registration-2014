$(document).ready(function(){

  function createTeam(){

    $.ajax({
      url:'/teams',
      type: 'POST',
      contentType:'application/json',
      dataType: 'json',
      success: function(){
        location.reload();
      }
    })
  }

  function leaveTeam(){

    $.ajax({
      url:'/team/leave',
      type: 'POST',
      contentType:'application/json',
      dataType: 'json',
      success: function(message){
        dimmerMessage(
          message.message,
          "",
          function(){
            location.reload();
          }, 1500
        )
      }
    })
  }

  function joinTeam(){

    $.ajax({
      url:'/teams/' + $('#teamInviteCode').val(),
      type: 'POST',
      contentType:'application/json',
      dataType: 'json',
      success: function(message){
        dimmerMessage(
          message.message,
          "",
          function(){
            location.reload();
          }, 1500
        );

      },
      error: function(error) {
        var msg = JSON.parse(error.responseText).message;
        $('.ui.form')
          .addClass('error')
          .form('add errors', [
            msg
          ])
      }
    })
  }

  $('#create').click(function(){
    createTeam();
  });

  $('#leave').click(function(){
    leaveTeam();
  });

  $('.ui.join.form')
    .form({
      code: {
        identifier: 'teamInviteCode',
        rules: [
          {
            type: 'empty',
            prompt: 'Please enter an invite code!'
          }
        ]
      }
    },{
      onSuccess: joinTeam
    })

});