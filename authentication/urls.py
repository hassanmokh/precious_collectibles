from django.urls import path
from .views import *

app_name = 'authentication'
urlpatterns = [
    path("register/", RegisterView.as_view(), name='register'),
    path("login/", LoginAPIView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),

    # verifications urls
    path("verify/email/", VerifyEmailView.as_view(), name="verify_email"),
    path("verification/resend/", ResendVerificationEmailView.as_view(), name="resend_email"),

    # Reset password
    path('password-reset/', ResetPasswordRequestToken.as_view(), name='reset_password'),
    path('password-reset/validate-token/', ResetPasswordValidateToken.as_view(), name='reset_password_validate_token'),
    path('password-reset/confirm/', ResetPasswordConfirm.as_view(), name='reset_password_confirm'),

]

