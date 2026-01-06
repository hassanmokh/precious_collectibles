from rest_framework import serializers
from locations.models import Locations, City, Governorate

class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = "__all__"


class GovernorateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Governorate
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Locations
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['city'] = CitySerializer(instance=instance.city).data
        rep['governorate'] = GovernorateSerializer(instance=instance.governorate).data

        return rep