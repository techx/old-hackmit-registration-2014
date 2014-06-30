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
        dimmerMessage(message.message)
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
        dimmerMessage(message.message)
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

  function dimmerMessage(message){
    var dimmer = $('.ui.page.dimmer')
      .dimmer('show');
    dimmer.find('h1').html(message);
    setTimeout(function(){
      dimmer.dimmer('hide');
      location.reload();
    },1500);
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