from django.contrib.auth.signals import user_logged_out
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from api.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from rest_framework.views import APIView


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):

        request._auth.delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)

        request.session.flush()
        if hasattr(request, "user"):
            from django.contrib.auth.models import AnonymousUser

            request.user = AnonymousUser()

        return Response({
            "message": _("Successfully logout")
        })
