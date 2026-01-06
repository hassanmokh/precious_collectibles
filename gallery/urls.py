from django.urls import path
from .views import *


app_name = 'gallery'

urlpatterns = [
    path("album/all/", ListAlbumAPIView.as_view(), name="list-album"),
    path("album/<uuid:pk>/", GetAlbumAPIView.as_view(), name="get-album"),
    path("album/create/", CreateAlbumAPIView.as_view(), name="create-album"),
    path("album/<uuid:pk>/delete/", DeleteAlbumAPIView.as_view(), name="delete-album"),
    
    path("album/<uuid:pk>/photos/", ListLivePhotosAPIView.as_view(), name="list-album-photos"),
    path("photo/create/", CreatePhotoAPIView.as_view(), name="create-photo"),
    path("photo/<uuid:pk>/", GetPhotoAPIView.as_view(), name="get-photo"),
    path("photo/<uuid:pk>/delete/", DeletePhotoAPIView.as_view(), name="delete-photo"),
]
