from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from favorites.serializers import FavoriteSerializer
from api.permissions import IsActiveUser
from favorites.models import Favorites


class ListFavoritesView(ListAPIView):
    permission_classes = [IsActiveUser]
    serializer_class = FavoriteSerializer
    queryset = Favorites.objects.all()


class RetrieveFavoriteView(RetrieveAPIView):
    permission_classes = [IsActiveUser]
    serializer_class = FavoriteSerializer
    queryset = Favorites.objects.filter()


class CreateFavoriteView(CreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsActiveUser]

    def get_serializer(self, *args, **kwargs):
        if 'data' in kwargs:
            kwargs['data']['user'] = self.request.user.id

        return super().get_serializer(*args, **kwargs)