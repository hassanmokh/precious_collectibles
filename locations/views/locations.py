from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveAPIView,
    GenericAPIView
)
from api.filters import DjangoFilterBackend, LocationFilter
from rest_framework.mixins import UpdateModelMixin
from locations.serializers import LocationSerializer
from api.permissions import AllowAny, IsAdminUser
from locations.models import Locations


class ListLocationsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = LocationSerializer
    queryset = Locations.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LocationFilter


class CreateLocationView(CreateAPIView):
    serializer_class = LocationSerializer
    permission_classes = [IsAdminUser]
