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

  $('#create').click(function(){
    createTeam();
  })

});