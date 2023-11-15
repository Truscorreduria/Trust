from twilio.rest import Client
from django.conf import settings
from django.core.mail import EmailMessage

client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)


def dos_decimales(number):
    return "{0:.2f}".format(number)


def send_email(subject, receipt, html, files=None, fr=None):
    from_email = fr or 'info@truscorreduria.com'

    email = EmailMessage(
        subject=subject,
        body=html,
        from_email="Trust Corredurida de Seguros <%s>" % from_email,
        to=[receipt],
    )

    if files and len(files) > 0:
        for file in files:
            email.attach_file(file)
    return email.send()


def send_sms(text, number):
    client.messages.create(
        from_=settings.TWILIO_PHONE_NUMBER,
        to='+505' + number,
        body=text
    )