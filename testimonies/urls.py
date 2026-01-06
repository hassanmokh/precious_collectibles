from django.urls import path
from .views import *


app_name = "testimonies"

urlpatterns = [
    path("all/", ListTestimoniesView.as_view(), name="list_testimonies"),
    path("<int:pk>/", RetrieveTestimoniesView.as_view(), name="get_testimony"),
    path("create/", CreateTestimonyView.as_view(), name="create_testimony"),
    path("<int:pk>/change/", UpdateTestimonyView.as_view(), name="update_testimony"),
]
