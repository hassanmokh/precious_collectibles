from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, GenericAPIView
from api.filters import DjangoFilterBackend, BrandFilter
from rest_framework.mixins import UpdateModelMixin
from api.permissions import AllowAny, IsAdminUser
from brands.serializers import BrandSerializer
from brands.models import Brands


class ListBrandsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BrandSerializer
    queryset = Brands.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BrandFilter


class CreateBrandView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = BrandSerializer


class RetrieveBrandView(RetrieveAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = BrandSerializer
    queryset = Brands.objects.filter()


class UpdateBrandView(UpdateModelMixin, GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = BrandSerializer
    queryset = Brands.objects.filter()

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
