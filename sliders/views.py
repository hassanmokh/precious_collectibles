from api.permissions import AllowAny, IsActiveUser, IsAdminUser, IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from .serializers import SliderSerializer
from rest_framework import status
from .models import Slider


class ListSlidersAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SliderSerializer
    queryset = Slider.objects.live()
    

class CreateSliderAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsActiveUser, IsAdminUser]
    serializer_class = SliderSerializer


class DeleteProductPhoto(DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Slider.objects.live()
    
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