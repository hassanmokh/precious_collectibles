from django.urls import path
from .views import *


app_name = "brands"

urlpatterns = [
    path("all/", ListBrandsView.as_view(), name='list_brands'),
    path("create/", CreateBrandView.as_view(), name='create_brand'),
    path("<uuid:pk>/", RetrieveBrandView.as_view(), name='get_brand'),
    path("<uuid:pk>/change/", UpdateBrandView.as_view(), name='update_brand'),
]
