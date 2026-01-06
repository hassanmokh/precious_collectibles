from django.urls import path
from .views import *


app_name = "favorites"

urlpatterns = [
    path("all/", ListFavoritesView.as_view(), name='list_favorites'),
    path("<uuid:pk>/", RetrieveFavoriteView.as_view(), name='get_favorite'),
    path("create/", CreateFavoriteView.as_view(), name='create_favorite'),
]
