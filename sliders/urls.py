from django.urls import path
from .views import *

app_name = "slider"

urlpatterns = [
    path("all/", ListSlidersAPIView.as_view(), name="list_sliders"),
    path("create/", CreateSliderAPIView.as_view(), name="create_sliders")
]
