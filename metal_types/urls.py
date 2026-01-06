from django.urls import path
from .views import *


app_name = "metal_types"

urlpatterns = [
    path("all/", ListMetalTypesView.as_view(), name="list_metal_types"),
    path("create/", CreateMetalTypeView.as_view(), name="create_metal_type"),

]
