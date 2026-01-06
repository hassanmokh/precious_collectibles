from django.urls import path
from .views import *

app_name = "pricing"

urlpatterns = [
    path("all/", ListPricingAPIView.as_view(), name="list-pricing"),
    path("live/", LivePricingAPIView.as_view(), name="live-pricing"),
    path("create/", CreatePricingAPIView.as_view(), name="create-pricing")
    
]
