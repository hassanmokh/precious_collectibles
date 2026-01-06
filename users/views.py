from users.serializers import UserSerializer, ChangeUserPasswordSerializer
from api.permissions import IsAdminUser, IsAuthenticated, IsActiveUser
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.generics import ListAPIView, GenericAPIView
from api.filters import DjangoFilterBackend, UserFilter
from django.utils.translation import gettext_lazy as _
from users.models import User


class ListUsersView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter


class ChangeUserPasswordView(UpdateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangeUserPasswordSerializer

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        resp = self.partial_update(request, *args, **kwargs)
        resp.data = {
            "message": _("successfully updated")
        }
        return resp


class MyInfoView(RetrieveModelMixin, UpdateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
