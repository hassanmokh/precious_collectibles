from django.urls import path
from .views import *


app_name = "locations"

urlpatterns = [
    path("all/", ListLocationsView.as_view(), name='list_locations'),
    path('create/', CreateLocationView.as_view(), name='create_location'),
    
]
