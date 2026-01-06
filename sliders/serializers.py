from rest_framework import serializers
from .models import Slider


class SliderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Slider
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True, "required": False}
        }