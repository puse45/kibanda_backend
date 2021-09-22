import africastalking
import requests
from django.conf import settings

africastalking.initialize(username=settings.AT_USERNAME, api_key=settings.AT_API_KEY)


def send_message(msg, phone):

    try:
        sms = africastalking.SMS
        sms.send(msg, [phone], callback=on_finish)
    except Exception as e:
        print("ERROR", e)


# Or use it asynchronously
def on_finish(error, response):
    if error is not None:
        raise error
    print(response)
