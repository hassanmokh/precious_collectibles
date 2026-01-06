from django.urls import path
from .views import *

app_name = "balances"

urlpatterns = [
    path("all/", ListBalancesView.as_view(), name="list_balances"),
    path("create/", CreateBalanceView.as_view(), name="create_balance"),
    path("<uuid:pk>/", GetBalanceView.as_view(), name='get_balance'),
    path("<uuid:pk>/change/", UpdateBalanceView.as_view(), name='update_balance'),
]
