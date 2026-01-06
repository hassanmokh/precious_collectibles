from django.urls import path, include
from locations.views import (
    ListGovernorateView, ListCitiesView,
    CreateGovernorateView, CreateCityView
)
from django.conf import settings

app_name = "api_v1"

urlpatterns = [
    path("auth/", include("authentication.urls", namespace="authentication")),
    path("users/", include("users.urls", namespace="users")),
    path("balances/", include("balances.urls", namespace="balances")),
    path("metals/", include("metal_types.urls", namespace="metal_types")),
    path("brands/", include("brands.urls", namespace="brands")),
    path("faqs/", include("faqs.urls", namespace="faqs")),
    path("favorites/", include("favorites.urls", namespace="favorites")),
    path("locations/", include("locations.urls", namespace="locations")),
    path("products/", include("products.urls", namespace="products")),
    path("testimonies/", include("testimonies.urls", namespace="testimonies")),
    path("pricing/", include("pricing.urls", namespace="pricing")),
    path("gallery/", include("gallery.urls", namespace="gallery")),
    path("slider/", include("sliders.urls", namespace="slider")),

    # lookups
    path("cities/all/", ListCitiesView.as_view(), name='list_cities'),
    path("cities/create/", CreateCityView.as_view(), name='create_city'),
    path("governorates/all/", ListGovernorateView.as_view(), name='list_governorate'),
    path("governorates/create/", CreateGovernorateView.as_view(), name='create_governorate'),
]


if settings.DEBUG:
    from .swagger import schema_view
    
    urlpatterns = [
        path('swagger<format>/', schema_view.with_ui(cache_timeout=0), name="schema-json"),
        path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-docs"),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name="swagger-redoc"),
    ] + urlpatterns