$(document).ready(function() {

  function register(){
    // AJAX form submission here
    console.log("Register!");
  }

  $(".register")
    .transition('fade up in');

  function showError(error){
    console.log(error.reason);
  }

  $('.ui.form')
    .form({
      email: {
        identifier: 'email',
        rules: [
          {
            type: 'empty',
            prompt: "Please enter an email!"
          },
          {
            type: 'email',
            prompt: "That's not a valid email address :("
          }
        ]
      },
      password: {
        identifier: 'password',
        rules: [
          {
            type: 'empty',
            prompt: "Please enter a password!"
          }
        ]
      }
    },{
      onSuccess: register
    })


});