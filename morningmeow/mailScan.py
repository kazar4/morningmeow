from __future__ import print_function

import base64
import pickle
import os.path

import phonenumbers
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#If modifying these scopes, delete the file token.pickle.
import fileManage2
from emailText import handleMail

def scanMailAndDelete():
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
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

    # Call the Gmail API
    user_id = 'me'
    label_id_one = 'INBOX'
    label_id_two = 'UNREAD'

    # Getting all the unread messages from Inbox
    # labelIds can be changed accordingly
    unread_msgs = service.users().messages().list(userId='me', labelIds=[label_id_one, label_id_two]).execute()

    # We get a dictonary. Now reading values for the key 'messages'
    #print(len(unread_msgs))
    if (len(unread_msgs) > 1):
        mssg_list = unread_msgs['messages']
    else:
        mssg_list = [];

    #print("Total unread messages in inbox: ", str(len(mssg_list)))
    #print(mssg_list)

    final_list = []
    for mssg in mssg_list:
        temp_dict = {}
        m_id = mssg['id']  # get id of individual message
        message = service.users().messages().get(userId="me", id=m_id).execute()  # fetch the message using API
        payld = message['payload']  # get payload of the message
        headr = payld['headers']  # get header of the payload

        for three in headr:  # getting the Sender
            if three['name'] == 'From':
                msg_from = three['value']
                temp_dict['Sender'] = msg_from
            else:
                pass

        temp_dict['Snippet'] = message['snippet']  # fetching message snippet

        try:

            # Fetching message body
            mssg_parts = payld['parts']  # fetching the message parts
            part_one = mssg_parts[0]  # fetching first element of the part
            part_body = part_one['body']  # fetching body of the message
            part_data = part_body['data']  # fetching data from the body
            clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
            clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
            clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8
            soup = BeautifulSoup(clean_two, "lxml")
            mssg_body = soup.body()
            # mssg_body is a readible form of message body
            # depending on the end user's requirements, it can be further cleaned
            # using regex, beautiful soup, or any other method
            temp_dict['Message_body'] = mssg_body

        except:
            pass

        #print(temp_dict)
        final_list.append(temp_dict)  # This will create a dictonary item in the final list
        # This will mark the messagea as read
        service.users().messages().modify(userId="me", id=m_id, body={'removeLabelIds': ['UNREAD']}).execute()

    #print("Total messaged retrived: ", str(len(final_list)))
    #print(final_list)

    parsedList = []
    for dict in final_list:
        body_text = dict['Snippet']
        if 'STOP' in body_text:
            arr = dict['Sender'].split('@')
            number = arr[0].strip()
            print(number)
            try:
                h = phonenumbers.parse("+1{}".format(number))
                print(h)
                if phonenumbers.is_valid_number(h):
                    if (fileManage2.checkNumber(number)):
                        handleMail(fileManage2.returnVals(number), "end")
                        fileManage2.deleteData(number)
                        print("Deleting {} from Database".format(number))
            except Exception as inst:
                print(type(inst))    # the exception instance
                print(inst.args)     # arguments stored in .args
                print(inst)
                print("Possible KeyError is trying to delete a number via mail that was setup via premium")
                print("Only deletes phonenumbers, not {}".format(number))
        elif 'BUG' in body_text:
            arr = dict['Sender'].split('@')
            number = arr[0]
            #print(number)
            try:
                h = phonenumbers.parse("+1{}".format(number))
                if phonenumbers.is_valid_number(h):
                    fileManage2.addBugReport(number, "mail", body_text)
                else:
                    fileManage2.addBugReport("none, mail error", "mail", body_text)
            except Exception as inst:
                print(type(inst))    # the exception instance
                print(inst.args)     # arguments stored in .args
                print(inst)
                print("Error saving bug log with: {}, BUG: {}".format(number, body_text))