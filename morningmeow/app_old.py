#import gevent.monkey
#gevent.monkey.patch_all()

from flask import Flask, request
from twilio import twiml

from gevent.pywsgi import WSGIServer

import fileManage2
import mailScan

from flask_cors import CORS
from flask_cors import cross_origin

import ssl

app = Flask(__name__)
cors = CORS(app)

@app.route('/sms', methods=['POST'])
@cross_origin()
def sms():
    numberRAW = request.form['From']

    number = numberRAW.split("+1")[1]
    message_body = request.form['Body']

    if (fileManage2.checkNumber(number)):
        if "STOP" in message_body:
            fileManage2.deleteData(number)
            fileManage2.addEndDateLog(number)
            print("SMS text included this body: {}".format(message_body))
            print("Deleting {} from Database".format(number))

    return "got text"

@app.route('/mail', methods=['POST'])
@cross_origin()
def mail():
    mailScan.scanMailAndDelete()
    return "got mail"

@app.route('/test', methods=['GET'])
@cross_origin()
def test():
    #mailScan.scanMailAndDelete()
    return "test is working"

if __name__ == '__main__':
    #app.run()
    test_kwargs = {'certfile': 'server.crt', 'keyfile': 'server.key',
                   'ca_certs': 'server.ca-bundle',
                   'ssl_version': ssl.PROTOCOL_TLSv1}

    http_server = WSGIServer(('localhost', 5000), app, **test_kwargs)
    http_server.serve_forever()


