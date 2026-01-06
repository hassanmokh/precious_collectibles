from rest_framework import serializers
from faqs.models import Faqs


class FaqsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Faqs
        fields = "__all__"
