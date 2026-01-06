from django_rest_passwordreset.signals import reset_password_token_created
from django.template.loader import render_to_string
from django.dispatch import receiver
from django.conf import settings
from .tasks import send_email


@receiver(reset_password_token_created)
def password_reset_token(sender, instance, reset_password_token, *args, **kwargs):

    context = {
        'app_name': settings.APP_NAME.capitalize(),
        'email_contact_us': settings.EMAIL_CONTACT_US,
        'token': reset_password_token.key,
        'display_name': reset_password_token.user.username
    }
    print("#####")
    body = render_to_string('users/user_reset_password.html', context)
    send_email.delay(subject=f"Password Reset for {settings.APP_NAME.capitalize()}",
                     email=reset_password_token.user.email,
                     body=body)

