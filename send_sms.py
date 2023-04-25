import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure


def message_from_vendor(message,costumer_phone):
    account_sid = os.environ['TWILIO_ACCOUNT_SID'] 
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    twilio_number = os.environ['TWILIO_PHONE']

    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body= message,
                        from_=twilio_number,
                        to=costumer_phone
                    )

    print(message.sid)
