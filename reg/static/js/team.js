$(document).ready(function(){
  $('.team')
    .transition('fade in');

  function createTeam(){

    $.ajax({
      url:'/teams',
      type: 'POST',
      contentType:'application/json',
      dataType: 'json',
      success: function(){
        location.reload();
      },
      error: function(error) {
        var msg = JSON.parse(error.responseText).message;
        showError(msg);
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
        var dimmer = $('.ui.page.dimmer')
          .dimmer('show');
        dimmer.find('h1').html(message.message);
        setTimeout(function(){
          dimmer.dimmer('hide');
          location.reload();
        },1500);
      },
      error: function(error) {
        var msg = JSON.parse(error.responseText).message;
        showError(msg);
      }
    })

  }

  $('#create').click(function(){
    createTeam();
  })

  $('#leave').click(function(){
    leaveTeam();
  })

});