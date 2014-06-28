$(document).ready(function() {

  function login(){
    // Form submission here
    console.log("login");
  }

  function showError(error){
    // Show an error on the DOM
  }

  // Do when template is rendered
  $(".login")
    .transition('fade up in');

  $('.ui.form')
    .form({
      email: {
        identifier: 'email',
        rules: [
          {
            type: 'empty',
            prompt: "Please enter your email!"
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
            prompt: "Please enter your password!"
          }
        ]
      }
    },{
      onSuccess: login
    });
})
