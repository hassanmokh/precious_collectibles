from django.urls import path
from .views import *


app_name = "users"

urlpatterns = [
    path("all/", ListUsersView.as_view(), name="list_view"),
    path("password/change/", ChangeUserPasswordView.as_view(), name="password_change"),
    path("my-info/", MyInfoView.as_view(), name="my_info"),
]
