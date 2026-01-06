from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from .permissions import AllowAny


schema_view = get_schema_view(openapi.Info(
    title="Precious Collectibles API",
    default_version="v1",
    description="This is a all api's in version 1",
    contact=openapi.Contact(email="hassan.mokhtar996@gmail.com"),
    license=openapi.License(name="MIT License")
), public=True, permission_classes=(AllowAny,))



__all__ = [
    'schema_view',
]
