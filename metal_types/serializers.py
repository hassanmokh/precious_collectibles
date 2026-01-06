from metal_types.models import MetalTypes
from rest_framework import serializers


class MetalTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MetalTypes
        fields = "__all__"
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "is_deleted": {"read_only": True},
            "photo": {"required": True}
        }
