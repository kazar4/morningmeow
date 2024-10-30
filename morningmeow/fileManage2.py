import os.path
import pickle
import sqlite3
import datetime

from pytz import timezone
from datetime import datetime, timedelta

from emailText import handleMail
from twilioText import handleMMS

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import stripe
import time as t

from PIL import Image, ExifTags
from PIL.ExifTags import TAGS

from util import readAuthFiles

listOfCarriersNoPremium = ['Sprint Spectrum, L.P.']

Carrier_Gateway = {'AT&T Wireless': 'mms.att.net',
                 'Verizon Wireless': 'vzwpix.com',
                 'T-Mobile USA, Inc': 'tmomail.net',
                 'Cricket Wireless - ATT - SVR': 'mms.cricketwireless.net',
                 'Sprint Spectrum, L.P.': 'pm.sprint.com'}

maxDay = 30;

stripe.api_key = readAuthFiles("./authFiles.txt")["stripe_secret_key"]


welcome_text = "Hello {}, and welcome to " \
                "MorningMeow! respond with \"STOP.\" to cancel.\n\n" \
                "More information can be found at https://morningmeow.com\n\n" \
                "\n\nHere is a message from the person who signed you up:\n\n{}"

#\n\nIf you find a bug or issue "
#             'it would help us a lot if you could send a text back as follows \n"BUG (issue here without parentheses)"' \

day_pass_text = "Thanks for sticking with us for these last {} days, if you enjoyed the cats and it helped brighten your mornings, please consider signing up again, at morningmeow.com"
#day_pass_text = "Here is your last cat for , if you enjoyed these past {} days and it helped brighten your mornings, please consider signing up again, at morningmeow.com"

goodbye_text = "You have opted out of MorningMeow. Thank you for giving us a chance, and we will alway still be here if you decide you want some cat pictures again!"

bug_text = "Bug Report Received, Thank You!"


'''
   if type == "reg":
        if day_pass != fileManage2.maxDay:
            sendMail(number, carrier, "", day)
        elif day_pass == fileManage2.maxDay:
            sendMail(number, carrier, "The {} days of beta are up, here is your last cat" \
                                      "if you liked the service please sign up at launch!".format(fileManage2.maxDay), day)
            fileManage2.deleteData(number)
    elif type == "welcome":
        sendMail(number, carrier, "Welcome to the 5 day beta of " \
                                  "MorningMeow! respond with STOP to cancel. " \
				  "Here is a message from the person who signed you up:\n\n{}".format(message), day)
    elif type == "end":
        sendMail(number, carrier, "Goodbye, its been real", -1)
        fileManage2.deleteData(number)
    elif type == "bug":
        print("attempting to send bug report response")
        sendMail(number, carrier, "Bug Report Received, Thank You!", -1)
'''


def addData(number, name, message, timezone, carrier, premium, pay_id):
    conn = sqlite3.connect('test2.db')
    #print("Opened database successfully")

    newTimetext = calculateNextDayText(timezone)

    conn.execute("INSERT INTO DATABASE (PHONE_NUMBER, NAME, MESSAGE, TIMEZONE, CARRIER, PREMIUM, SEND_TIME, CAN_SEND, DAY_PASS, DAY, PAY_ID) \
            VALUES(?, ?, ?, ?, ?, ?, ?, 'false', 1, ?, ?);", (number, name, message, timezone, carrier, premium, newTimetext, getGlobalDay(), pay_id))
    conn.commit()

    saveLog(number, name, message, timezone, carrier, premium, pay_id)

    row = [number, name, message, timezone, carrier, premium, newTimetext, "NA", 0, getGlobalDay()]
    welcome(row)

    #addData("4017827071", "Kazen", "Hello", "Place", "AT&T", "NP")

def deleteData(number):
    addEndDateLog(number)
    
    conn = sqlite3.connect('test2.db')
    conn.execute("DELETE from DATABASE where PHONE_NUMBER = ?;", [number])
    conn.commit()
    print("Total number of rows deleted :", conn.total_changes)
    #print("Deleting {} from Database".format(number))

def checkNumber(number):
    conn = sqlite3.connect('test2.db')
    value = conn.execute(
    "SELECT CASE WHEN EXISTS (SELECT * FROM DATABASE WHERE PHONE_NUMBER = ?) \
    THEN CAST(1 AS BIT) \
    ELSE CAST(0 AS BIT) END;", [number])
    for row in value:
        returnVal = row[0]

    conn.commit()
    if (returnVal == 1):
        return True
    else:
        return False

#signup num

def changeBool(number, value):
    conn = sqlite3.connect('test2.db')
    conn.execute("UPDATE DATABASE set CAN_SEND = ? where PHONE_NUMBER = ?;", (value, number))
    conn.commit()
    conn.close()

def changeSendTime(number, value):
    conn = sqlite3.connect('test2.db')
    conn.execute("UPDATE DATABASE set SEND_TIME = ? where PHONE_NUMBER = ?;", (value, number))
    conn.commit()
    conn.close()

def incrementDay(number):
    conn = sqlite3.connect('test2.db')
    value = conn.execute(
        "SELECT DAY FROM DATABASE WHERE PHONE_NUMBER = ?;", [number])
    day = 0;
    for row in value:
        day = row[0]
    day = day + 1
    conn.execute("UPDATE DATABASE set DAY = ? where PHONE_NUMBER = ?;", (day, number))
    conn.commit()

def incrementDayPass(number):
    conn = sqlite3.connect('test2.db')
    value = conn.execute(
        "SELECT DAY_PASS FROM DATABASE WHERE PHONE_NUMBER = ?;", [number])
    day = 0;
    for row in value:
        day = row[0]
    day = day + 1
    conn.execute("UPDATE DATABASE set DAY_PASS = ? where PHONE_NUMBER = ?;", (day, number))
    conn.commit()

# def getDay(number):
#     conn = sqlite3.connect('test2.db')
#     value = conn.execute(
#         "SELECT DAY FROM DATABASE WHERE PHONE_NUMBER = ?;", [number])
#     day = 0;
#     for row in value:
#         day = row[0]
#     conn.commit()
#     return day

def saveLog(number, name, message, timezone, carrier, premium, pay_id):
    conn = sqlite3.connect('test2.db')
    #print("Opened database successfully")

    timezoneData = 'US/Eastern';
    c = datetime.now()
    c.strftime("%b %d %Y %H:%M:%S")

    conn.execute("INSERT INTO DATABASE_LOG (PHONE_NUMBER, NAME, MESSAGE, TIMEZONE, CARRIER, PREMIUM, DATE_DATA, END_DATE, FINAL, PAY_ID) \
                    VALUES(?, ?, ?, ?, ?, ?, ?, '', 'false', ?);", (number, name, message, timezone,
                                                                                 carrier, premium,
                                                                              c.strftime("%b/%d/%Y %H:%M:%S"), pay_id))
    conn.commit()

def addEndDateLog(number):
    timezoneData = 'US/Eastern';
    c = datetime.now()
    timeVal = c.strftime("%b/%d/%Y %H:%M:%S")

    conn = sqlite3.connect('test2.db')
    conn.execute("UPDATE DATABASE_LOG set END_DATE = ? where PHONE_NUMBER = ? AND FINAL = 'false';", (timeVal, number))
    conn.commit()
    conn.execute("UPDATE DATABASE_LOG set FINAL = ? where PHONE_NUMBER = ?;", ('true', number))
    conn.commit()

def updateAllToTrue():
    conn = sqlite3.connect('test2.db')
    conn.execute("UPDATE DATABASE set CAN_SEND = 'true';")
    conn.commit()
    #conn.close()

def returnVals(number):
    conn = sqlite3.connect('test2.db')
    value = conn.execute(
        "SELECT * FROM DATABASE WHERE PHONE_NUMBER = ?;", [number])
    array = []
    for row in value:
        array = row
    print(array)

    conn.commit()
    return array

def arrayOfDatabaseTrue():
    conn = sqlite3.connect('test2.db')
    value = conn.execute(
        "SELECT * FROM DATABASE WHERE CAN_SEND = 'true';")
    array = [];
    for row in value:
        array.append(row)
    conn.commit()
    conn.close()
    return array

def arrayOfDatabaseTrueNEW():
    conn = sqlite3.connect('test2.db')
    value = conn.execute(
        "SELECT * FROM DATABASE WHERE CAN_SEND = 'true';")

    conn.commit()
    conn.close()
    return value

def arrayOfDatabase():
    conn = sqlite3.connect('test2.db')
    value = conn.execute(
        "SELECT * FROM DATABASE;")
    array = [];
    for row in value:
        array.append(row)
    conn.commit()
    conn.close()
    return array

def arrayOfDatabaseNEW():
    conn = sqlite3.connect('test2.db')
    value = conn.execute(
        "SELECT * FROM DATABASE;")
    conn.commit()
    return value

def sendMessage(row):
    premium = row[5]
    if premium == "P":
        handleMMS(row, "reg")
    elif premium == "NP":
        handleMail(row, "reg")

def welcome(row):
    premium = row[5]
    number = row[0]

    incrementDay(number)
    incrementDayPass(number)

    if premium == "P":
        handleMMS(row, "welcome")
    elif premium == "NP":
        handleMail(row, "welcome")

def calculateNextDayText(tz):
    c = datetime.now(timezone(tz))
    df = c + timedelta(days=1)
    newTime = datetime(df.year, df.month, df.day, 9, 55)
    #newTime = datetime(df.year, df.month, df.day, df.hour, df.minute)
    newTimeText = newTime.strftime("%d/%m/%y %H:%M")
    return newTimeText

def activateWatch():
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    request = {
        'labelIds': ['INBOX'],
        'topicName': 'projects/quickstart-1598843570656/topics/quickstart'
    }
    val = service.users().watch(userId='me', body=request).execute()

def getGlobalDay():
    conn = sqlite3.connect('test2.db')
    value = conn.execute(
        "SELECT DAY_VAL FROM DAY;")
    day = 0
    for row in value:
        day = row[0]
    conn.commit()
    return day

def addPhoneCache(number, carrier):
    conn = sqlite3.connect('test2.db')
    conn.execute("INSERT INTO PHONE_CACHE (PHONE_NUMBER, CARRIER) \
                VALUES(?,?);", (number, carrier))
    conn.commit()

def checkPhoneCache(number):
        conn = sqlite3.connect('test2.db')
        value = conn.execute(
            "SELECT * FROM PHONE_CACHE WHERE PHONE_NUMBER = ?;", [number])
        array = None
        for row in value:
            array = row

        conn.commit()
        return array

def clearPhoneCache():
    conn = sqlite3.connect('test2.db')
    conn.execute("DELETE from PHONE_CACHE")
    conn.commit()

    changes = conn.total_changes
    print("Phone Cache deleted {} Records".format(changes))

    return changes
    # print("Deleting {} from Database".format(number))



def addConfirmedPaymentIntent(ID, clientSecret):
    conn = sqlite3.connect('test2.db')
    conn.execute("INSERT INTO PAYMENT_INTENTS (ID, INTENT) \
                VALUES(?,?);", (ID, clientSecret))
    conn.commit()

def removeConfirmedPaymentIntent(clientSecret):
    conn = sqlite3.connect('test2.db')
    conn.execute("DELETE from PAYMENT_INTENTS where INTENT = ?;", [clientSecret])
    conn.commit()
    print("Total number of rows deleted :", conn.total_changes)
    #print("Deleting {} from Database".format(number))

def getConfirmedPaymentIntentID(clientSecret):
    conn = sqlite3.connect('test2.db')
    value = conn.execute(
        "SELECT ID FROM PAYMENT_INTENTS WHERE INTENT = ?;", [clientSecret])
    ID = "";
    for row in value:
        ID = row[0]
    conn.commit()
    return ID

def removeAllConfirmedPaymentIntent(clientSecret):
    conn = sqlite3.connect('test2.db')
    conn.execute("DELETE from PAYMENT_INTENTS")
    conn.commit()

    changes = conn.total_changes
    print("Payment Intents deleted {} Records".format(changes))

    return changes
    # print("Deleting {} from Database".format(number))

def checkConfirmedPaymentIntent(clientSecret):
    conn = sqlite3.connect('test2.db')
    value = conn.execute(
    "SELECT CASE WHEN EXISTS (SELECT * FROM PAYMENT_INTENTS WHERE INTENT = ?) \
    THEN CAST(1 AS BIT) \
    ELSE CAST(0 AS BIT) END;", [clientSecret])
    for row in value:
        returnVal = row[0]

    conn.commit()
    if (returnVal == 1):
        return True
    else:
        return False

def cancelPaymentAndRemove(clientSecret):
    t_end = t.time() + 60 * 0.15
    while t.time() < t_end:
        ID = getConfirmedPaymentIntentID(clientSecret)
        if (ID != ""):
            intent = stripe.PaymentIntent.cancel(ID)
            removeConfirmedPaymentIntent(clientSecret)
            break      


def getMetaData(day):
    img = Image.open("../html/MCI/{}.jpg".format(day))
    #exifdata = image.getexif()
    #img = Image.open("image.jpg")

    #print(dir(img))
    # [... 'getexif' ...]

    #print(img.info)

    comment = b'\x00'

    img_exif = img.getexif()
    if img_exif:
        #print(type(img_exif))
        # <class 'PIL.Image.Exif'>
        #print(dict(img_exif))
        # { .. 271: 'FUJIFILM', 305: 'Adobe Photoshop Lightroom 6.14 (Macintosh)', }

        img_exif_dict = dict(img_exif)
        for key, val in img_exif_dict.items():
            if key in ExifTags.TAGS:
                #print(ExifTags.TAGS[key] + " - " + str(val))
                if (ExifTags.TAGS[key] == "XPComment"):
                    comment = val
    else:
        print("Sorry, image has no exif data.")

    return comment.replace(b'\x00', b'').decode('utf-8')

def addBugReport(number, type, bug_report_full):
    bug_report = bug_report_full.replace('BUG', '').strip()

    timezoneData = 'US/Eastern';
    c = datetime.now()
    timeVal = c.strftime("%b/%d/%Y %H:%M:%S")

    conn = sqlite3.connect('test2.db')
    conn.execute("INSERT INTO BUG_REPORT (PHONE_NUMBER, BUG, TIME) \
                VALUES(?,?,?);", (number, type.upper() + ": " + bug_report, timeVal))
    conn.commit()

    if (type == "mail") and (number != "none, mail error"):
        handleMail(returnVals(number), "bug")
    elif type == "sms":
        handleMMS(returnVals(number), "bug")
