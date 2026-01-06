from rest_framework.generics import ListAPIView, CreateAPIView
from .serializers import ListPricingSerializers, CreatePricingSerializers
from api.permissions import IsAuthenticated, IsActiveUser, IsAdminUser, AllowAny
from .models import Pricing


class ListPricingAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsActiveUser, IsAdminUser]
    serializer_class = ListPricingSerializers
    queryset = Pricing.objects.all()


class CreatePricingAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsActiveUser, IsAdminUser]
    serializer_class = CreatePricingSerializers


class LivePricingAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ListPricingSerializers
    queryset = Pricing.objects.filter(old=False)
