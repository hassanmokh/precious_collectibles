from rest_framework.generics import ListAPIView, CreateAPIView
from api.filters import DjangoFilterBackend, CityFilter
from locations.serializers import CitySerializer
from api.permissions import IsAdminUser
from locations.models import City

class ListCitiesView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CityFilter

    
class CreateCityView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CitySerializer