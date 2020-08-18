// Wait for the DOM to be ready
jQuery.validator.addMethod("lettersonly", function(value, element) {
  return this.optional(element) || /^[a-z]+$/i.test(value);
}); 

jQuery.validator.addMethod("firstalphabet", function(value, element) {
  return this.optional(element) || /^[a-zA-Z][a-zA-Z0-9.,$;_#]+$/i.test(value);
}); 



$(function() {
    // Initialize form validation on the registration form.
    // It has the name attribute "registration"
    $("form[name='signup']").validate({
      // Specify validation rules
      rules: {
        // The key name on the left side is the name attribute
        // of an input field. Validation rules are defined
        // on the right side
        uname: {
          required: true,
          firstalphabet: true
        },
        pwd: {
            required: true,
            minlength: 5
        },
        fname:{
          lettersonly: true,
          required: true,
        },
        lname: {
          lettersonly: true,
          required: true,
        },
        mob: {
            required: true,
            minlength: 10,
            maxlength: 10,
            number: true
        },
        email: {
          required: true,
          // Specify that email should be validated
          // by the built-in "email" rule
          email: true
        },
        dob:"required"
        
      },
      // Specify validation error messages
      messages: {
        uname: {
          required: "Please enter your username",
          firstalphabet: "Username should start with alphabet and you can use only .,$;_# special characters",
        }, 
        fname:{
          required: "Please enter your firstname",
          lettersonly: "Letters only please",
        }, 
        lname: {
          required: "Please enter your lastname",
          lettersonly: "Letters only please",
        }, 
        pwd: {
          required: "Please provide a password",
          minlength: "Your password must be at least 5 characters long"
        },
        mob: {
            required: "Please provide your mobile number",
            minlength: "please provide valid mobile number",
            maxlength: "please provide valid mobile number",
            number: "please provide valid mobile number"
        },
        email: "Please enter a valid email address",
        dob: "please enter your date of birth"
      },
      // Make sure the form is submitted to the destination defined
      // in the "action" attribute of the form when valid
      submitHandler: function(form) {
        form.submit();
      }
    });

    $("form[name='editprofile']").validate({
      // Specify validation rules
      rules: {
        // The key name on the left side is the name attribute
        // of an input field. Validation rules are defined
        // on the right side
        pwd: {
            required: true,
            minlength: 5
        },
        fname: {
          lettersonly: true,
          required: true,
        },
        lname: {
          lettersonly: true,
          required: true,
        },
        mob: {
            required: true,
            minlength: 10,
            maxlength: 10,
            number: true
        },
        email: {
          required: true,
          // Specify that email should be validated
          // by the built-in "email" rule
          email: true
        },
        dob:"required"
        
      },
      // Specify validation error messages
      messages: {
        fname:  {
          required: "Please enter your firstname",
          lettersonly: "Letters only please",
        }, 
        lname:  {
          required: "Please enter your lastname",
          lettersonly: "Letters only please",
        }, 
        pwd: {
          required: "Please provide a password",
          minlength: "Your password must be at least 5 characters long"
        },
        mob: {
            required: "Please provide your mobile number",
            minlength: "please provide valid mobile number",
            maxlength: "please provide valid mobile number",
            number: "please provide valid mobile number"
        },
        email: "Please enter a valid email address",
        dob: "please enter your date of birth"
      },
      // Make sure the form is submitted to the destination defined
      // in the "action" attribute of the form when valid
      submitHandler: function(form) {
        form.submit();
      }
    });

  });