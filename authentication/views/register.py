from knox.views import LoginView as KnoxLoginView
from users.serializers import RegisterSerializer
from django.contrib.auth import login
from api.permissions import AllowAny
from rest_framework.settings import api_settings


class RegisterView(KnoxLoginView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def get_post_response_data(self, request, token, instance):

        UserSerializer = self.get_user_serializer_class()

        data = {
            'token': token
        }
        if UserSerializer is not None:
            data["user"] = UserSerializer(
                request.user,
                context=self.get_context()
            ).data
        return data

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return (user, headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, format=None):

        user, headers = self.create(request)

        login(request, user)

        resp = super().post(request, format)
        resp.headers = headers
        # send email verification
        user.send_email_verification()
        return resp



