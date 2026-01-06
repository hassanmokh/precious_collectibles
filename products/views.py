from products.serializers import ProductSerializer, ProductPhotosSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from api.filters import DjangoFilterBackend, ProductFilter
from django.utils.translation import gettext_lazy as _
from products.models import Products, ProductPhotos
from api.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

class ListProducts(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    queryset = Products.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter

class CreateProduct(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer

class CreateProductPhotos(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductPhotosSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message": "successfully created"}, status=status.HTTP_201_CREATED)


class DeleteProductPhoto(DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = ProductPhotos.objects.live()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_deleted:
            return Response({"message": "It's already deleted!"}, status=status.HTTP_400_BAD_REQUEST)

        resp = super().destroy(request, *args, **kwargs)
        resp.status_code = 200
        resp.data = {
            "message": _("successfully deleted")
        }

        return resp

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
