from twilio.rest import Client
from util import readAuthFiles

import fileManage2

def handleMMS(row, type):

    day = row[9]
    day_pass = row[8]
    number = row[0]
    message = row[2]
    name = row[1]

    if type == "reg":
        if day_pass != fileManage2.maxDay:
            sendMMS(number, "", day)
        elif day_pass == fileManage2.maxDay:
            sendMMS(number, fileManage2.day_pass_text.format(fileManage2.maxDay), 0)
            fileManage2.deleteData(number)
    elif type == "welcome":
        sendMMS(number, fileManage2.welcome_text.format(name, message), day)
    elif type == "end":
        sendMMS(number, fileManage2.goodbye_text, -1)
        fileManage2.deleteData(number)
    elif type == "bug":
        sendMMS(number, fileManage2.bug_text, -1)

def sendMMS(number, text, day):
    # Your Account SID from twilio.com/console
    account_sid = readAuthFiles("./authFiles.txt")["twilio_account_sid"]
    # Your Auth Token from twilio.com/console
    auth_token = readAuthFiles("./authFiles.txt")["twilio_auth_token"]

    client = Client(account_sid, auth_token)

    if text != "" and day != -1:
        message = client.messages.create(
            to="+1" + str(number),
            from_="+14012082404",
            body = text,
            media_url=['https://morningmeow.com/MCI/{}.jpg'.format(day)])
    elif text == "" and day != -1:
        message = client.messages.create(
            to="+1" + str(number),
            from_="+14012082404",
            media_url=['https://morningmeow.com/MCI/{}.jpg'.format(day)])
    else:
        message = client.messages.create(
            to="+1" + str(number),
            from_="+14012082404",
            body=text)

    print(message.sid)

