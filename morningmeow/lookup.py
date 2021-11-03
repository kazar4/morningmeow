from twilio.rest import Client

"""
phone_number = client.lookups \
                     .phone_numbers('+17746415184') \
                     .fetch(type=['carrier'])

print(phone_number.carrier) # All of the carrier info.
print(phone_number.carrier['name']) # Just the carrier name.
"""

def look(number):
    # Your Account SID from twilio.com/console
    account_sid = "SK83af3f72432b39001de0b6cd758db8be"
    # Your Auth Token from twilio.com/console
    auth_token = "6Oh2f1u1y09AWnpdv1xKrC3gFu8xpQXg"

    client = Client(account_sid, auth_token)

    phone_number = client.lookups \
        .phone_numbers('+1' + str(number)) \
        .fetch(type=['carrier'])
    return phone_number.carrier['name']