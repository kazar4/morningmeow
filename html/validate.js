form = document.getElementById("main-form");

name_val = document.getElementById("name");
phone_number = document.getElementById("number");
timezone = document.getElementById("timezoneVal");
timezoneText = document.getElementById("timezoneDefText");
timezoneOuter = document.getElementById("timezoneOuter");
terms_val = document.getElementById("terms");
termsOuter = document.getElementById("termsOuter");

function validateNoPremium() {
    if(!validateForm()) {
        // If it isn't, we display an appropriate error message
        //showError();
        // Then we prevent the form from being sent by canceling the event
      } else {
          connect()
      }
}

`
form.addEventListener('click', function (event) {
    // if the email field is valid, we let the form submit
    console.log("form submitted");
  
    if(!validateForm()) {
      // If it isn't, we display an appropriate error message
      //showError();
      // Then we prevent the form from being sent by canceling the event
      event.preventDefault();
    } else {
        connect()
    }
  });
`

function validateForm(){
    nameBool = false;
    numberBool = false;
    timezoneBool = false;
    termsBool = false;

    if (name_val.value != ""){
        console.log("valid name")
        nameBool = true;
    } else {
        name_val.placeholder = "Please Input a Name"
        name_val.style.border = "medium inset #0056b3";
    }
    if (/^[0-9]{10}$/.test(phone_number.value)){
        console.log("valid phone number")
        numberBool = true;
    } else {
        phone_number.value = "";
        phone_number.placeholder = "Invalid, Ex: 0001112222"
        phone_number.style.border = "medium inset #0056b3";
    }
    if (getTimezoneText() != "Timezone"){     
        console.log("valid timezone")
        timezoneBool = true;
    } else {
        timezoneText.innerHTML = "Timezone is Required"
        timezoneOuter.style.border = "medium inset #0056b3";
    }

    if (terms_val.checked == true) {
        termsBool = true;
    } else {
        termsOuter.style.border = "medium inset #0056b3";
    }

    return nameBool && numberBool && timezoneBool && termsBool
}


name_val.addEventListener("focus", function (event) {
    name_val.placeholder = "Name (Recipient)"
    name_val.style.border = "none";
});
phone_number.addEventListener("focus", function (event) {
    phone_number.placeholder = "Phone Number"
    phone_number.style.border = "none";
});
timezone.addEventListener("focus", function (event) {
    timezoneText.innerHTML = "Timezone"
    timezoneOuter.style.border = "none";
});