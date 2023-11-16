from twilio.rest import Client
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)


def dos_decimales(number):
    return "{0:.2f}".format(number)


def send_email(subject, receipt, html, files=None, fr=None):
    from_email = fr or 'info@truscorreduria.com'
    text_version = strip_tags(html)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_version,
        from_email="Trust Corredurida de Seguros <%s>" % from_email,
        to=[receipt],
    )
    email.attach_alternative(html, "text/html")

    if files:
        for file in files:
            email.attach(file.name, file.read(), file.content_type)
    return email.send()


def send_sms(text, number):
    client.messages.create(
        from_=settings.TWILIO_PHONE_NUMBER,
        to='+505' + number,
        body=text
    )