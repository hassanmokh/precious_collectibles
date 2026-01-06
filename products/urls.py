from django.urls import path
from .views import *


app_name = "products"

urlpatterns = [

    path("all/", ListProducts.as_view(), name="list_products"),
    path("create/", CreateProduct.as_view(), name="create_product"),
    path("photos/create/", CreateProductPhotos.as_view(), name="create_product_photos"),
    path("photo/<uuid:pk>/delete/", DeleteProductPhoto.as_view(), name="delete_product_photos")
]
