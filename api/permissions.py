from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly,
    BasePermission
)


class IsActiveUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and
                    request.user.is_authenticated and
                    request.user.is_email_verified and
                    not request.user.is_deleted
                    )


__all__ = [
    'AllowAny',
    'IsAuthenticated',
    'IsAdminUser',
    'IsAuthenticatedOrReadOnly',
    'IsActiveUser',
]

