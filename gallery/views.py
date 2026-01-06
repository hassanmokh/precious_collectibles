from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from api.permissions import IsAuthenticated, IsActiveUser, AllowAny, IsAdminUser
from .serializers import AlbumSerializer, PhotoSerializer
from .models import Album, Photo
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class ListAlbumAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AlbumSerializer
    queryset = Album.objects.live()


class GetAlbumAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = AlbumSerializer
    queryset = Album.objects.live()
    

class CreateAlbumAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsActiveUser, IsAdminUser]
    serializer_class = AlbumSerializer
    

class DeleteAlbumAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsActiveUser, IsAdminUser]
    queryset = Album.objects.live()
    
    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({
            "message": "Successfully deleted"
            },status=status.HTTP_200_OK)


class ListLivePhotosAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PhotoSerializer
    queryset = Photo.objects
    
    def get_queryset(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(Album.objects.live(), **filter_kwargs)
        return self.queryset.live(album_id=obj.id)

class CreatePhotoAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsActiveUser, IsAdminUser]
    serializer_class = PhotoSerializer
    

class GetPhotoAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = PhotoSerializer
    queryset = Photo.objects.live()
    

class DeletePhotoAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsActiveUser, IsAdminUser]
    queryset = Photo.objects.live()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response({
            "message": "Successfully deleted"
            },status=status.HTTP_200_OK)