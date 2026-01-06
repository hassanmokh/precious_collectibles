from rest_framework import serializers
from rest_framework.fields import empty
from brands.models import Brands
from django.utils.translation import gettext_lazy as _


class BrandSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Brands
        fields = "__all__"
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "is_deleted": {"read_only": True},
            "photo": {"required": True}
        }

    def validate(self, attrs):

        attrs = super().validate(attrs)

        if self.partial and not attrs:
            raise serializers.ValidationError({"message": _("You should update at least one field")})
        
        return attrs
