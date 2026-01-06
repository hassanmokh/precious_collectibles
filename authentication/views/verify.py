from django.utils.translation import gettext_lazy as _
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from api.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.utils.timezone import now


class VerifyEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user

        if request.data.get("code", None) is None:
           return Response({
                "message": _("Invalid data sent!")
            }, status=HTTP_400_BAD_REQUEST)

        elif user.verification_code != request.data.get("code"):
            return Response({
                "message": _("Invalid verification code")
            }, status=HTTP_400_BAD_REQUEST)

        elif user.is_email_verified:
            return Response({
                "message": _("Your email already verified!")
            }, status=HTTP_400_BAD_REQUEST)

        elif user.expire_verification_code and user.expire_verification_code < now():
            return Response({
                "message": _("Your code was expired")
            }, status=HTTP_400_BAD_REQUEST)


        user.verification_code = None
        user.expire_verification_code = None
        user.is_email_verified = True
        user.save()

        return Response({
            "message": _("Successfully verified")
        })


class ResendVerificationEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user

        if not user.send_email_verification():
            return Response({
                "message": _("Your email already verified")
            }, status=HTTP_400_BAD_REQUEST)

        else:
            return Response({
                "message": _("Email has been sent. Please check your mailbox.")
            })