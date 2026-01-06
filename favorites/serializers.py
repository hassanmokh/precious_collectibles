from products.serializers import ProductSerializer
from rest_framework import serializers
from favorites.models import Favorites


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorites
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        del rep['user']
        rep['product'] = ProductSerializer(instance=instance.product).data

        return rep