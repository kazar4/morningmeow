from flask import Flask, request
from twilio import twiml

import sys
sys.path.append("..")

import fileManage2
import mailScan

from flask_cors import CORS
from flask_cors import cross_origin

import stripe

app = Flask(__name__)
cors = CORS(app)

#run this in CL with wgsi.py to start server [gunicorn --bind 0.0.0.0:5000 --certfile=server.crt --keyfile=server.key --ca-certs=server.ca-bundle wsgi:app]

@app.route('/sms', methods=['POST'])
@cross_origin()
def sms():
    print('/sms')

    numberRAW = request.form['From']

    number = numberRAW.split("+1")[1]
    message_body = request.form['Body']

    if "STOP" in message_body and fileManage2.checkNumber(number):
        fileManage2.deleteData(number)
        print("SMS text included this body: {}".format(message_body))
        print("Deleting {} from Database".format(number))
    elif "BUG" in message_body:
        fileManage2.addBugReport(number, "sms", message_body)

    return "got text"

@app.route('/mail', methods=['POST'])
@cross_origin()
def mail():
    print('/mail')

    mailScan.scanMailAndDelete()
    return "got mail"

@app.route('/test', methods=['GET'])
@cross_origin()
def test():
    #mailScan.scanMailAndDelete()
    return "test is working"


# You can find your endpoint's secret in your webhook settings
endpoint_secret = 'whsec_bEDWmpuh2ocNrMBHwsxm2hfIBRfYON4v'

@app.route("/webhook", methods=['POST'])
@cross_origin()
def webhook():
  print("/webhook")
  payload = request.get_data()
  sig_header = request.headers.get('STRIPE_SIGNATURE')
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # invalid payload
    return "Invalid payload", 400
  except stripe.error.SignatureVerificationError as e:
    # invalid signature
    return "Invalid signature", 400

  event_dict = event.to_dict()
  if event_dict['type'] == "payment_intent.amount_capturable_updated":
    intent = event_dict['data']['object']
    print("Succeeded: ", intent['id'])
    print("Client Secret: ", intent['client_secret'])
    fileManage2.addConfirmedPaymentIntent(intent['id'], intent['client_secret'])
    # Fulfill the customer's purchase

  elif event_dict['type'] == "payment_intent.payment_failed":
    intent = event_dict['data']['object']
    error_message = intent['last_payment_error']['message'] if intent.get('last_payment_error') else None
    print("Failed: ", intent['id'], error_message)
    # Notify the customer that payment failed

  return "OK", 200

@app.route('/dailyImage', methods=['GET'])
@cross_origin()
def getImage():
    image_day = fileManage2.getGlobalDay()
    return str(image_day) + '|' + fileManage2.getMetaData(image_day)   
    #str(fileManage2.getGlobalDay())

if __name__ == '__main__':
    app.run(host='0.0.0.0')