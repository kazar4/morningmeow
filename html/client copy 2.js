function checkPremium() {
  var checkbox = document.getElementById('premium');
  if (checkbox.checked == true){
    allowPayment();
    document.getElementById('signup').disabled = true;
    document.getElementById('signup').style.display = "none";

    document.getElementById('all-payment').disabled = false;
    document.getElementById('all-payment').style.display = "block";
  } else {
    document.getElementById('signup').disabled = false;
    document.getElementById('signup').style.display = "block";

    document.getElementById('all-payment').disabled = true;
    document.getElementById('all-payment').style.display = "none";
  }
}

function getPremiumVal() {
  var checkbox = document.getElementById('premium');
  if (checkbox.checked == true){
    return "P";
  } else {
    return "NP";
  }
}

`
function handleClickConfirm(connectVal) {
  if (connectVal == '3'){
    console.log("Purchsae can be made")
    allowPayment()
    prButton.submit()
  }
}
`
var clientSecret = "";
function getClientSecret() {
  return clientSecret;
}

function allowPayment() {

var paymentRequest = stripe.paymentRequest({
  country: 'US',
  currency: 'usd',
  total: {
    label: 'Demo total',
    amount: 200,
  },
});

var elements = stripe.elements();
var prButton = elements.create('paymentRequestButton', {
  paymentRequest: paymentRequest,
});

prButton.on('click', function(event) {
  console.log("Button Clicked");
  //connect();
  //prButton.submit();
});

// Check the availability of the Payment Request API first.
paymentRequest.canMakePayment().then(function(result) {
  if (result) {
    prButton.mount('#payment-request-button');

  var response = fetch('https://morningmeow.com:3000/secret').then(function(response) {
  return response.json();
}).then(function(responseJson) {
  clientSecret = responseJson.client_secret;

  paymentRequest.on('paymentmethod', function(ev) {
    // Confirm the PaymentIntent without handling potential next actions (yet).
    //Work on cool stuff
    
    stripe.confirmCardPayment(
      clientSecret,
      {payment_method: ev.paymentMethod.id},
      {handleActions: false}
    ).then(function(confirmResult) {
      if (confirmResult.error) {
        // Report to the browser that the payment failed, prompting it to
        // re-show the payment interface, or show an error message and close
        // the payment interface.
        ev.complete('fail');
      } else {
        // Report to the browser that the confirmation was successful, prompting
        // it to close the browser payment method collection interface.
        ev.complete('success');
        // Let Stripe.js handle the rest of the payment flow.
        stripe.confirmCardPayment(clientSecret).then(function(result) {
          if (result.error) {
            // The payment failed -- ask your customer for a new payment method.
            allowPayment()
          } else {
            // The payment has succeeded.
            console.log("Payment success")
            console.log(clientSecret)
            connect();
            allowPayment()
          }
        });
      }
    });
  });
});
  } else {

  document.getElementById('payment-request-button').style.display = 'none';
  console.log("Cannot use payment button")

  paymentReg();

     // Set up Stripe.js and Elements to use in checkout form
  var style = {
    base: {
      color: "#32325d",
    }
  };

  var card = elements.create("card", { style: style });
  card.mount("#card-element");

  var response = fetch('https://morningmeow.com:3000/secret').then(function(response) {
  return response.json();
}).then(function(responseJson) {
  var clientSecret = responseJson.client_secret;
  var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
  ev.preventDefault();
  stripe.confirmCardPayment(clientSecret, {
    payment_method: {
      card: card,
      billing_details: {
        name: 'Jenny Rosen'
      }
    }
  }).then(function(result) { 
    if (result.error) {
      console.log("this is where error is ")
      // Show error to your customer (e.g., insufficient funds)
      console.log(result.error.message);
      allowPayment()

    } else {
      // The payment has been processed!
      if (result.paymentIntent.status === 'succeeded') {
        console.log("Payment success")
        connect();
        allowPayment()
        // Show a success message to your customer
        // There's a risk of the customer closing the window before callback
        // execution. Set up a webhook or plugin to listen for the
        // payment_intent.succeeded event that handles any business critical
        // post-payment actions.
      }
    }
  });
});
});


  }
});
}

function paymentReg(){
  const paymentDiv = document.getElementById("payment-regular")

  paymentDiv.innerHTML = `

  <form id="payment-form">
  <div id="card-element">
    <!-- Elements will create input elements here -->
  </div>

  <!-- We'll put the error messages in this element -->
  <div id="card-errors" role="alert"></div>

  <div class="container-contact100-form-btn">
					<button class="contact100-form-btn" type="button" id="submit" onclick="connect()">
						<span>
							<i class="fa fa-paper-plane-o m-r-6" aria-hidden="true"></i>
							Pay!
						</span>
					</button>
				</div>

  `;
}

//person doesnt use premium
//use connect() on sign up

// Person clicks apple pay
// connect() is run
// confirmation on server side before 3 is returned
// if 3 is returned run a function that submits pay button


// Person clicks pay button
// connect() is run
// confirmation on server side before 3 is returned
// if 3 is returned run a function acts as the submit button id event

