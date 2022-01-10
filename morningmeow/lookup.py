from twilio.rest import Client
from util import readAuthFiles

"""
phone_number = client.lookups \
                     .phone_numbers('+17746415184') \
                     .fetch(type=['carrier'])

print(phone_number.carrier) # All of the carrier info.
print(phone_number.carrier['name']) # Just the carrier name.
"""

def look(number):
    # Your Account SID from twilio.com/console
    account_sid = readAuthFiles("./authFiles.txt")["twilio_account_sid"]
    # Your Auth Token from twilio.com/console
    auth_token = readAuthFiles("./authFiles.txt")["twilio_auth_token"]

    client = Client(account_sid, auth_token)

    phone_number = client.lookups \
        .phone_numbers('+1' + str(number)) \
        .fetch(type=['carrier'])
    return phone_number.carrier['name']