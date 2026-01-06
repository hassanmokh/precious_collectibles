from metal_types.serializers import MetalTypeSerializer
from brands.serializers import BrandSerializer
from rest_framework import serializers
from products.models import Products, ProductPhotos
from django.conf import settings
from decimal import Decimal


class ProductPhotosSerializer(serializers.ModelSerializer):
    
    photos = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True, required=True
    )
        
    class Meta:
        model = ProductPhotos
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True, "required": False},
            "created_at": {"read_only": True},
            "is_deleted": {"read_only": True},
            "photo": {"read_only": True}
        }

    
    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)
    
    def create(self, validated_data):
        product = validated_data['product']
        last = []
        for ph in validated_data['photos']:
            last.append(super().create({
                "product": product,
                "photo": ph
            }))
        return last

class ProductSerializer(serializers.ModelSerializer):
    photos = ProductPhotosSerializer(many=True, required=False, source="live_photos")
    price = serializers.SerializerMethodField()
    fees = serializers.SerializerMethodField()
    
    class Meta:
        model = Products
        fields = "__all__"
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "is_deleted": {"read_only": True},
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['metal_type'] = MetalTypeSerializer(instance=instance.metal_type).data
        rep['brand'] = BrandSerializer(instance=instance.brand).data
        return rep

        
    def get_price(self, instance):
        price_gold = instance.get_live_gold_price
        prive_silver = instance.get_live_silver_price
        
        if instance.metal_type.name.lower().__contains__('gold'):
            if instance.kirat == 24:
                return round(Decimal(instance.weight) * (price_gold['local_buy'] * settings.KIRAT_24_FROM_21))
            elif instance.kirat == 18:
                return round(Decimal(instance.weight) * (price_gold['local_buy'] * settings.KIRAT_18_FROM_21))
            else:
                return round(Decimal(instance.weight) * price_gold['local_buy'])
        
        elif instance.metal_type.name.lower().__contains__('silver'):
            return round(Decimal(instance.weight) * prive_silver['local_buy'])
        
        return

    
    def get_fees(self, instance):
        obj = instance.get_manufacture_fees
        data = {}
        for fee in obj:
            data.update({
                "fees": fee['fees'],
                "cashback": fee['cashback'],
                "total_fees": round(Decimal(instance.weight) * fee['fees']),
                "total_cashback":  round(Decimal(instance.weight) * fee['cashback'])
            })
            
        return data
        