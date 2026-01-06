from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView, GenericAPIView, DestroyAPIView
)
from api.filters import DjangoFilterBackend, FaqsFilter
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.utils.translation import gettext_lazy as _
from rest_framework.mixins import UpdateModelMixin
from api.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from faqs.serializers import FaqsSerializer
from faqs.models import Faqs


class ListFaqsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = FaqsSerializer
    queryset = Faqs.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FaqsFilter


class RetrieveFaqView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = FaqsSerializer
    queryset = Faqs.objects.filter()


class UsefulFaqsView(UpdateModelMixin, GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = FaqsSerializer
    queryset = Faqs.objects.filter()

    def get_serializer(self, *args, **kwargs):
        kwargs['data']['num_useful'] = self.get_object().num_useful + 1
        return super().get_serializer(*args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class UnusefulFaqsView(UpdateModelMixin, GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = FaqsSerializer
    queryset = Faqs.objects.filter()

    def get_serializer(self, *args, **kwargs):
        kwargs['data']['num_unuseful'] = self.get_object().num_unuseful + 1
        return super().get_serializer(*args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CreateFaqsView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = FaqsSerializer


class DeleteFaqView(DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Faqs.objects.filter()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_deleted:
            return Response({"message": "It's already deleted!"}, status=HTTP_400_BAD_REQUEST)

        resp = super().destroy(request, *args, **kwargs)
        resp.status_code = 200
        resp.data = {
            "message": _("successfully deleted")
        }

        return resp

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

