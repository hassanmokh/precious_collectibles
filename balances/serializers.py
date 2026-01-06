from django.utils.translation import gettext_lazy as _
from products.serializers import ProductSerializer
from rest_framework import serializers
from balances.models import Balances


class BalanceSerializers(serializers.ModelSerializer):

    class Meta:
        model = Balances
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        del rep['user']
        rep['product'] = ProductSerializer(instance=instance.product).data

        return rep

    def create(self, validated_data):
        validated_data['is_available'] = True
        return super().create(validated_data)


class UpdateBalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Balances
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
            "id": {"read_only": True},
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        del rep['user']
        rep['product'] = ProductSerializer(instance=instance.product).data

        return rep

    def validate_is_available(self, value):
        if self.instance.is_available == value:
            raise serializers.ValidationError(_(f"It's already {value.__str__().lower()}"))

        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if self.partial and not attrs:
            raise serializers.ValidationError({"message": _("You should update at least one field")})

        return attrs
