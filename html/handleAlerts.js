const modalDiv = document.getElementById("modal_text");

var modal = document.getElementById("myModal");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
function togglePopup() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

infoText =
`<p>While we want MorningMeow to be free, some carriers block texts from services like MorningMeow automatically.
<br>
<br>
To get around this a separate service is used that costs money per text.
<br>
<br>
Purchasing premium allows us to pay for this service and fund future projects. Note, this is not a subscription, and you will only be billed once.
<br>
<br>
Message and data rates may apply.
</p>`

phoneUsedText =
`
<p> The entered phone number has already been signed up, please use another.</p>
`

needPremiumText =
`
<p> The given phone number uses a carrier that requires premium, for more information click <button onclick="changeDiv(9)" style="color: #bdbdd3; background:none; border:none;">here</button> or the (more info) text to learn more.</p>
`

signUpText =
`
<p> Congrats! the number given has been sucessfully signed up for Morning Meow, a cat will be sent shortly </p>
`

errorText =
`
<p> An error has occured, make sure all forms are filled out. Please reload the webpage and try again! If the problem persists for longer than a day, please contact morningmeow0@gmail.com so we can make the service better! <br> <br> If the text went through but you have noticed a bug in the service please send a text back explaining the problem with the text "BUG" in it</p>
`

generalInfoText =
`
<p style="font-weight:bold; font-size:17px; color:#5D5D5D;"> Welcome to Morning Meow! </p>
<br>
<p>Morning Meow was first created to send cat photos to some friends, but we quickly realized that others would enjoy it too. It became the perfect project during the corona-crisis-- as rising college students, both hoping to expand our respective skills in programming and art.</p>
<br>
<p>Heres how it works, use the form on this page to sign up yourself (or a friend) with an optional message, then every morning at 10am in the timezone you give, the phone number will receive a picture of a cat!</p>
<br>
<p>While the days of YouTube compilations and kitten TikToks (admit it ;) are far from over, we hope Morning Meow can add a little kick to your mornings with each and every kitten picture!! </p>
<br>
<p>Thanks for sticking with us throughout this adventure, and of course, please thank and check out Morning Corgi (<a href="https://www.morningcorgi.com/" style="color: #bdbdd3; background:none; border:none;">www.morningcorgi.com</a>) as they inspired us!</p>
<br>
<p>Thanks again,</p>
<p>Morning Meow</p>
`

questionText =
`
<p style="font-weight:bold; font-size:20px; color:#5D5D5D;"> Questions! </p><br>
<p style="font-weight:bold; font-size:15px; color:#4C4C4C;">Who is this for?</p>
<p>Anyone! You can sign up yourself or a friend, leaving them a heartfelt message and passing on the fun!</p>
<br>
<p style="font-weight:bold; font-size:15px; color:#4C4C4C;">Do I need a subscription?</p>
<p>Nope, a subscription is only needed if your phone carrier blocks the cats we send. To get around this we have to use a paid service for those carriers. For more information check <button onclick="changeDiv(9)" style="color: #bdbdd3; background:none; border:none;">here</button></p>
<br>
<p style="font-weight:bold; font-size:15px; color:#4C4C4C;">Where does my payment info go?</p>
<p>We actually never see your payment info at all, as it is all done securely via stripe (similar to paypal). So you can sleep tight knowing that your information is secure so that your cat experience can continue to be enjoyable</p>
<br>
<p style="font-weight:bold; font-size:15px; color:#4C4C4C;">Want your cat featured?</p>
<p>Email <a href="mailto:morningmeow0@gmail.com" style="color: #bdbdd3;">morningmeow0@gmail.com</a> with a picture of your cat so that we can add the picture to our queue! 
All cats used are either royalty free or user featured, to find out where they are from, go to <a href="dailyImage.html" style="color: #bdbdd3;">Cat of The Day!</a></p>
<br>
<p style="font-weight:bold; font-size:15px; color:#4C4C4C;">Can I cancel?</p>
<p>Yep, reply to the text with STOP and the service will end, with the really sad side effect of not receiving cats anymore :(</p>
`

//modalDiv.innerHTML = infoText


function changeDiv(value){
    if (value == 1){
        modalDiv.innerHTML = phoneUsedText
        togglePopup()
    }
    if (value == 2){
        modalDiv.innerHTML = needPremiumText
        togglePopup()
    }
    if (value == 3){
        modalDiv.innerHTML = signUpText
        togglePopup()
    }
    if (value == 4){
        modalDiv.innerHTML = errorText
        togglePopup()
    }
    if (value == 9){
        modalDiv.innerHTML = infoText
        togglePopup()
    }
    if (value == 10){
      modalDiv.innerHTML = generalInfoText
      togglePopup()
    }
    if (value == 11){
      modalDiv.innerHTML = questionText
      togglePopup()
    }
}
