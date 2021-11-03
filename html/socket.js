async function connect(){

    let numberVal = document.getElementById("number").value;
    let nameVal = document.getElementById("name").value;
    let messageVal = document.getElementById("message").value;
    //remember to make it check for message greater than x length befroe sending so
    //people cannot exploit server by spamming long messages
    let timezoneVal = getTimezoneText();
    let premiumVal = getPremiumVal();
    let clientSecretVal = getClientSecret()

    value = "9";

    console.log(nameVal + ": " + numberVal)
                //messages = document.createElement('ul');

                //var ws = new WebSocket("ws://127.0.0.1:5678/")
                var ws = new WebSocket("wss://morningmeow.com:5678/")
                ws.onopen = function(event) {
                    ws.send(numberVal);
                    ws.send(premiumVal);
                    ws.send(clientSecretVal);
                  };

                ws.onmessage = function (event) {
                    //console.log("onmessage:")
                    value = String(event.data);
                    console.log(value);
                    
                    if (value == "1"){
                        console.log("phone number in use");
                        changeDiv(value);
                    } else if (value == "2") {
                        console.log("Carrier requires premium");
                        changeDiv(value);
                    } else if (value == "3") {
                        console.log("No Problems! Signing You Up");
                        ws.send(numberVal);
                        ws.send(nameVal);
                        ws.send(messageVal);
                        ws.send(timezoneVal);
                        ws.send(premiumVal);
                        changeDiv(value);
                    } else if (value == "4") {
                        changeDiv(value);
                    } else {
                        changeDiv("4");
                        //get it to send a webhook
                        console.log("error occurred");
                    }

                    //if (premiumVal == 'P' && value == 3){
                    //    continuePayment();
                    //}

                    //handleClickConfirm(value)
                    //return(value)
                    //ws.close();
        
                };

            
  }
