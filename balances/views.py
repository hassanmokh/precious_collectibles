from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    GenericAPIView
)
from balances.serializers import BalanceSerializers, UpdateBalanceSerializer
from rest_framework.mixins import UpdateModelMixin
from api.permissions import IsActiveUser
from balances.models import Balances
from api.filters import DjangoFilterBackend, BalanceFilter

class ListBalancesView(ListAPIView):
    permission_classes = [IsActiveUser]
    serializer_class = BalanceSerializers
    queryset = Balances.objects
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BalanceFilter

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)


class GetBalanceView(RetrieveAPIView):
    permission_classes = [IsActiveUser]
    serializer_class = BalanceSerializers
    queryset = Balances.objects

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)


class CreateBalanceView(CreateAPIView):
    permission_classes = [IsActiveUser]
    serializer_class = BalanceSerializers

    def get_serializer(self, *args, **kwargs):
        kwargs['data']['user'] = self.request.user.id

        return super().get_serializer(*args, **kwargs)


class UpdateBalanceView(UpdateModelMixin, GenericAPIView):
    permission_classes = [IsActiveUser]
    serializer_class = UpdateBalanceSerializer
    queryset = Balances.objects

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
