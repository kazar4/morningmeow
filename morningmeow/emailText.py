import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from util import readAuthFiles

import fileManage2

def handleMail(row, type):

    day = row[9]
    day_pass = row[8]
    number = row[0]
    carrier = row[4]
    message = row[2]
    name = row[1]

    if type == "reg":
        if day_pass != fileManage2.maxDay:
            sendMail(number, carrier, "", day)
        elif day_pass == fileManage2.maxDay:
            sendMail(number, carrier, fileManage2.day_pass_text.format(fileManage2.maxDay), day)
            fileManage2.deleteData(number)
    elif type == "welcome":
        sendMail(number, carrier, fileManage2.welcome_text.format(name, message), day)
    elif type == "end":
        sendMail(number, carrier, fileManage2.goodbye_text, -1)
        fileManage2.deleteData(number)
    elif type == "bug":
        print("attempting to send bug report response")
        sendMail(number, carrier, fileManage2.bug_text, -1)

def sendMail(number, carrier, text, day):
    #setup
    email = "morningmeow0"
    pas = readAuthFiles("./authFiles.txt")["morningmeow0@gmail.com_pass"]
    sms_gateway = '{}@{}'.format(number, fileManage2.Carrier_Gateway[carrier])

    #make server
    smtp = "smtp.gmail.com"
    port = 587
    server = smtplib.SMTP(smtp,port)
    server.starttls()
    server.login(email,pas)

    if text != "":
        msg = MIMEMultipart()
        msg['To'] = sms_gateway
        msg.attach(MIMEText(text))
        sms = msg.as_string()
        server.sendmail(email, sms_gateway, sms)
    if day != -1:
        msg = MIMEMultipart()
        msg['To'] = sms_gateway
        msg.attach(MIMEImage(open("MCI/{}.jpg".format(day), 'rb').read()))
        sms = msg.as_string()
        server.sendmail(email, sms_gateway, sms)

    server.quit()
