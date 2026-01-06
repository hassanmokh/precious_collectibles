from rest_framework.generics import ListAPIView, CreateAPIView
from api.filters import DjangoFilterBackend, GovernorateFilter
from locations.serializers import GovernorateSerializer
from api.permissions import IsAdminUser
from locations.models import Governorate


class ListGovernorateView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = GovernorateSerializer
    queryset = Governorate.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GovernorateFilter


class CreateGovernorateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = GovernorateSerializer