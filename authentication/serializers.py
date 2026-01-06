from django_rest_passwordreset.serializers import PasswordTokenSerializer as OldTokenSerializer
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class PasswordTokenSerializer(OldTokenSerializer):
    password = serializers.CharField(label=_("Password"),
                                     style={'input_type': 'password'},
                                     validators=[validate_password])
    password1 = serializers.CharField(label=_("Password1"), style={'input_type': 'password'})
    token = serializers.CharField()

    def validate(self, data):
        data = super().validate(data)

        if data['password'] != data['password1']:
            raise serializers.ValidationError({
                "message": _("Password fields didn't match")
            })

        return data
