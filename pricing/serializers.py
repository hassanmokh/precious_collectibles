from rest_framework import serializers
from .models import Pricing
from django.conf import settings

class ListPricingSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Pricing
        fields = ("type", "local_sell", "local_buy", "world_sell", "world_buy", "old", "created_at")

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['type'] = instance.get_type_display()
        if instance.type == 1:
            rep['buy_kirat_24'] = round(instance.local_buy * settings.KIRAT_24_FROM_21)
            rep['buy_kirat_18'] = round(instance.local_buy * settings.KIRAT_18_FROM_21)
            rep['sell_kirat_24'] = round(instance.local_sell * settings.KIRAT_24_FROM_21)
            rep['sell_kirat_18'] = round(instance.local_sell * settings.KIRAT_18_FROM_21)
            
        return rep

class CreatePricingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = ("type", "local_sell", "local_buy", "world_sell", "world_buy")
        extar_kwargs = {
            "world_sell": {"required": False},
            "world_buy": {"required": False},
        }
    
    def to_representation(self, instance):
        
        rep =  super().to_representation(instance)
        
        rep['type'] = instance.get_type_display()
        
        return rep