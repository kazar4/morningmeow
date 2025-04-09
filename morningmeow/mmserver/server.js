// Set your secret key. Remember to switch to your live secret key in production!
// See your keys here: https://dashboard.stripe.com/account/apikeys

const express = require('express');
var cors = require('cors');
var fs = require('fs')
var https = require('https')
const app = express();

var auth_dict = {}

fs.readFile('../authFiles.txt', 'utf8' , (err, data) => {
  if (err) {
    console.log("GPT HEsadkqsjdhqwjoeilEEEEEEEEEEEE")
    console.error(err)
    return
  }

  let temp_data = data.split('\n')
  temp_data = temp_data.map(l => l.trim())
  for (let i=0; i < temp_data.length; i++) {
    let k = temp_data[i].split(":")[0]
    let v = temp_data[i].split(":")[1]
    auth_dict[k] = v
  }

  const stripe = require('stripe')(auth_dict['stripe_secret_key']);

  var allowedOrigins = ['http://morningmeow.com:3000', 'http://morningmeow.com', 'https://morningmeow.com:3000', 'https://morningmeow.com']
  app.use(cors({
      origin: function (origin, callback){
          if (!origin) return callback(null, true);

          if(allowedOrigins.indexOf(origin) === -1){
              var msg = 'The COS policty for this site does not ' +
              'allow adcess from the specified Origin.';
              return callback(new Error(msg), false);
          }
          return callback(null, true)
      }

  }));

  app.get('/secret', async (req, res) => {

    const intent = await stripe.paymentIntents.create({
      amount: 40000,
      currency: 'usd',
      capture_method:'manual',
      // Verify your integration in this guide by including this parameter
      metadata: {integration_check: 'accept_a_payment'},
    });

    res.json({client_secret: intent.client_secret});
  });

  https.createServer({
    key: fs.readFileSync(auth_dict["server_key_path"]),
    cert: fs.readFileSync(auth_dict["server_crt_path"])
  }, app).listen(3000, () => {
    console.log('Running on port 3000');
  });
})
