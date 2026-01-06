from rest_framework import serializers
from charts.models import Charts
from decimal import Decimal


def convert_from_24_to_21(price_24):
    return (price_24 * 875 / Decimal(999.9)).quantize(Decimal(".01"))


def calculate_price_gm_24_from_21(price):
    return (price * Decimal(999.9 / 875)).quantize(Decimal(".01"))


def calculate_price_gm_24_from_ounce(price):
    return (price / Decimal("31.1")).quantize(Decimal(".01"))


def calculate_price_gm_21_from_24(price):
    return ((price * 875) / Decimal("999.9")).quantize(Decimal(".01"))


def calculate_price_gm_18_from_21(price):
    return (price * Decimal(6/7)).quantize(Decimal(".01"))


def calculate_price_gm_18_from_ounce(price):
    return calculate_price_gm_18_from_21(calculate_price_gm_21_from_24(calculate_price_gm_24_from_ounce(price)))


def calculate_price_gm_21_from_ounce(price):
    return calculate_price_gm_21_from_24(calculate_price_gm_24_from_ounce(price))


def calculate_price_ounce(price):
    """
    :param price: is a price 24 for one gm
    :return: decimal for price ounce (31.1)
    """
    return (price * Decimal("31.1")).quantize(Decimal(".01"))


class ChartsSerializer(serializers.ModelSerializer):
    world_buy_price_18 = serializers.SerializerMethodField()
    world_buy_price_24 = serializers.SerializerMethodField()
    world_buy_price_21 = serializers.SerializerMethodField()
    world_buy_price_ounce = serializers.SerializerMethodField()
    local_buy_price_18 = serializers.SerializerMethodField()
    local_buy_price_24 = serializers.SerializerMethodField()
    local_buy_price_21 = serializers.SerializerMethodField()
    local_buy_price_ounce = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = Charts
        exclude = ('world_sell_price', 'world_buy_price', 'local_buy_price', 'local_sell_price')
        read_only_fields = [
            'id',
            'type',
        ]

    def get_world_buy_price_18(self, obj):
        return f"{calculate_price_gm_18_from_ounce(obj.world_buy_price)}$"

    def get_world_buy_price_24(self, obj):
        return f"{calculate_price_gm_24_from_ounce(obj.world_buy_price)}$"

    def get_world_buy_price_21(self, obj):
        return f"{calculate_price_gm_21_from_ounce(obj.world_buy_price)}$"

    def get_world_buy_price_ounce(self, obj):
        return f"{obj.world_buy_price}$"

    def get_local_buy_price_18(self, obj):
        return f"{calculate_price_gm_18_from_21(obj.local_buy_price)}EGP"

    def get_local_buy_price_24(self, obj):
        return f"{calculate_price_gm_24_from_21(obj.local_buy_price)}EGP"

    def get_local_buy_price_21(self, obj):
        return f"{obj.local_buy_price}EGP"

    def get_local_buy_price_ounce(self, obj):
        return f"{calculate_price_ounce(calculate_price_gm_24_from_21(obj.local_buy_price))}EGP"

    def get_type(self, obj):
        return obj.get_type_display()

