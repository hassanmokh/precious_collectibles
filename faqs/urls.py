from django.urls import path
from .views import *


app_name = "faqs"

urlpatterns = [
    path("all/", ListFaqsView.as_view(), name='list_faqs'),
    path("create/", CreateFaqsView.as_view(), name="create_faqs"),
    path("<uuid:pk>/", RetrieveFaqView.as_view(), name="get_faq"),
    path("<uuid:pk>/useful/", UsefulFaqsView.as_view(), name="useful_faq"),
    path("<uuid:pk>/unuseful/", UnusefulFaqsView.as_view(), name="unuseful_faq"),
    path("<uuid:pk>/delete/", DeleteFaqView.as_view(), name="delete_faq"),
]
