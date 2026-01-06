from rest_framework.generics import ListAPIView, CreateAPIView
from metal_types.serializers import MetalTypeSerializer
from api.permissions import AllowAny, IsAdminUser
from metal_types.models import MetalTypes


class ListMetalTypesView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = MetalTypeSerializer
    queryset = MetalTypes.objects.all()


class CreateMetalTypeView(CreateAPIView):
    serializer_class = MetalTypeSerializer
    permission_classes = [IsAdminUser]

