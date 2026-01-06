from django_rest_passwordreset.views import (
    ResetPasswordRequestToken, ResetPasswordConfirm as OldResetPasswordConfirm,
    ResetPasswordValidateToken
)
from .verify import VerifyEmailView, ResendVerificationEmailView
from authentication.serializers import PasswordTokenSerializer
from .register import RegisterView
from .login import LoginAPIView
from .logout import LogoutView


class ResetPasswordConfirm(OldResetPasswordConfirm):
    serializer_class = PasswordTokenSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

__all__ = [
    'LoginAPIView',
    'LogoutView',
    'RegisterView',
    'VerifyEmailView',
    'ResendVerificationEmailView',
    'ResetPasswordRequestToken',
    'ResetPasswordConfirm',
    'ResetPasswordValidateToken',

]
