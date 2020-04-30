// The following code show execute only after the page is fully loaded
alert('efwef');
$(document).ready(function () {
      alert('12');
      // Enable jQuery Validation for the form
      $('#submitForm').validate({ onkeyup: false });
  
      // Add validation rules to the Address field
      $("#address").rules("add", {
        fulladdress: true,
        messages: {
          fulladdress: "Google cannot locate this address."
        }
      });
  
      // This function will be executed when the form is submitted
      function FormSubmit() {
        alert("WHATTT");
        $.submitForm = true;
        if (!$('#submitForm').valid()) {
          return false;
        } else {
          if ($("#address").data("IsChecking") == true) {
            $("#address").data("SubmitForm", true);
            return false;
          }
  
          alert('Form is valid!');
          // return true;   // Uncomment to submit the form.
          return false;     // Supress the form submission for test purpose.
        }
      }

      // Execute the ForumSubmit function when the form is submitted
      $('#submitForm').submit(FormSubmit);
    
  });
  
  // Create a jQuery exists method
  jQuery.fn.exists = function () { return jQuery(this).length > 0; }
  
  // Address jQuery Validator
  function AddressValidator(value, element, paras) {
    
    alert('we here');
    // Convert the value variable into something a bit more descriptive
    var CurrentAddress = value;
  
    /* If the address is blank, then this is for the required validator to deal with. */
    if (value.length == 0) {
      return true;
    }
  

    /* We have a new address to validate, set the IsChecking flag to true and set the LastAddressValidated to the CurrentAddress */
    $(element).data("IsChecking", true);

  
    /* Create a new Google geocoder */
    var geocoder = new google.maps.Geocoder();
    alert('we');
    geocoder.geocode({ 'address': CurrentAddress }, function (results, status) {
  
      /* The code below only gets run after a successful Google service call has completed. Because this is an asynchronous call, the validator has already returned a 'true' result to supress an error message and then cancelled the form submission.  The code below needs to fetch the true validation from the Google service and then re-execute the jQuery form validator to display the error message.  Futhermore, if the form was 
      being submitted, the code below needs to resume that submit. */
  
      // Google reported a valid geocoded address
      if (status == google.maps.GeocoderStatus.OK) {
  

          // We have a valid geocoded address
          $(element).data("IsValid", true);
        // Otherwise the address is invalid
      } else {
        $(element).data("IsValid", false);
      }
  
      // We're no longer in the midst of validating
      $(element).data("IsChecking", false);
  
      // Get the parent form element for this address field
      var form = $(element).parents('form:first');
  
      /* This code is being run after the validation for this field, if the form was being submitted before this validtor was called then we need to re-submit the form. */
      if ($(element).data("SubmitForm") == true) {
        form.submit();
      } else {
        // Re-validate this property so we can return the result.
        form.validate().element(element);
      }
    });
  
    /* The Address validator always returns 'true' when initially called. The true result will be return later by the geocode function (above) */
    return true;
  }
  
  // Define a new jQuery Validator method
  $.validator.addMethod("fulladdress", AddressValidator);