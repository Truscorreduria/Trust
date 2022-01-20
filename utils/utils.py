import requests
from twilio.rest import Client
from django.conf import settings

client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)


def dos_decimales(number):
    return "{0:.2f}".format(number)


def send_simple_message(address):
    return requests.post(
        "https://api.mailgun.net/v3/trustcorreduria.com/messages",
        auth=("api", "338f0a7715e124eaf80cbaf279f274a1-7bbbcb78-a34c85e8"),
        data={"from": "Excited User <info@truscorreduria.com>",
              "to": [address, ],
              "subject": "Hello",
              "text": "Mensaje de prueba desde Mailgun!"})


def send_email(subject, receipt, html, files=None, fr=None):
    from_email = fr or 'info@truscorreduria.com'
    if files and len(files) > 0:
        return requests.post(
            "https://api.mailgun.net/v3/trustcorreduria.com/messages",
            auth=("api", "338f0a7715e124eaf80cbaf279f274a1-7bbbcb78-a34c85e8"),
            files=files,
            data={"from": "Trust Corredurida de Seguros <%s>" % from_email,
                  "to": receipt,
                  "subject": subject,
                  "html": html})
    else:
        return requests.post(
            "https://api.mailgun.net/v3/trustcorreduria.com/messages",
            auth=("api", "338f0a7715e124eaf80cbaf279f274a1-7bbbcb78-a34c85e8"),
            data={"from": "Trust Corredurida de Seguros <%s>" % from_email,
                  "to": receipt,
                  "subject": subject,
                  "html": html})


def send_sms(text, number):
    client.messages.create(
        from_=settings.TWILIO_PHONE_NUMBER,
        to='+505' + number,
        body=text
    )