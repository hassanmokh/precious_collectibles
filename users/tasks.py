from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from celery import shared_task

@shared_task
def send_email(subject, email, body, from_email=settings.DEFAULT_FROM_EMAIL):

    msg = EmailMultiAlternatives()
    msg.from_email = from_email
    msg.subject = subject
    msg.body = body
    msg.attach_alternative(body, 'text/html')

    if isinstance(email, list):
        msg.to = email

    else:
        msg.to = [email]

    msg.send()
