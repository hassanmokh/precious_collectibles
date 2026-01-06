from rest_framework.generics import ListAPIView, CreateAPIView, GenericAPIView, RetrieveAPIView
from testimonies.serializers import TestimoniesSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework.mixins import UpdateModelMixin
from api.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from testimonies.models import Testimonies


class ListTestimoniesView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TestimoniesSerializer
    queryset = Testimonies.objects.live()


class RetrieveTestimoniesView(RetrieveAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = TestimoniesSerializer
    queryset = Testimonies.objects.live()


class CreateTestimonyView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = TestimoniesSerializer


class UpdateTestimonyView(UpdateModelMixin, GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = TestimoniesSerializer
    queryset = Testimonies.objects.live()

    def patch(self, request, *args, **kwargs):

        resp = self.partial_update(request, *args, **kwargs)

        if "is_deleted" in self.request.data:
            resp.data = {
                "message": _("successfully deleted")
            }

        return resp
