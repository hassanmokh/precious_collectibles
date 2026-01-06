from django.utils.translation import gettext_lazy as _
from testimonies.models import Testimonies
from rest_framework import serializers
import re


class TestimoniesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Testimonies
        fields = "__all__"

    def validate_full_name(self, value):

        if len(value.split(" ")) < 2 or not re.match(r"^(?=.*[A-Za-z\-])(?=.*[\s]{0,})(?=.*[A-Za-z\-]).{6,50}$", value):
            raise serializers.ValidationError({
                "message": _("Please enter the correct full name, The length of the full name should at least 6 characters contains alphabets and - only")
            })

        return value

    def validate(self, attrs):

        attrs = super().validate(attrs)

        if self.partial and not attrs:
            raise serializers.ValidationError({"message": _("you should update at least one field")})

        return attrs
