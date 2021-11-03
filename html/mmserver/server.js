// Set your secret key. Remember to switch to your live secret key in production!
// See your keys here: https://dashboard.stripe.com/account/apikeys
const stripe = require('stripe')('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');

const express = require('express');
var cors = require('cors');
var fs = require('fs')
var https = require('https')
const app = express();

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
    amount: 200,
    currency: 'usd',
    capture_method:'manual',
    // Verify your integration in this guide by including this parameter
    metadata: {integration_check: 'accept_a_payment'},
  });

  res.json({client_secret: intent.client_secret});
});

https.createServer({
  key: fs.readFileSync('server.key'),
  cert: fs.readFileSync('server.crt')
}, app).listen(3000, () => {
  console.log('Running on port 3000');
});
