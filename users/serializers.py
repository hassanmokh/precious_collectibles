from rest_framework import serializers
from users.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from utils import validate_domain_email
from django.db.models import Q


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            # Read Only
            'username',

            # Read & Write
            'first_name', 'last_name',
            'email', 'is_email_verified',

        )

        extra_kwargs = {
            'username': {'read_only': True},
            'is_email_verified': {'read_only': True},
        }

    def validate_email(self, value):
        if User.objects.filter(~Q(id=self.instance.id) & Q(email=value)):
            raise serializers.ValidationError({"message": _("This email already exists")})

        return value

    def update(self, instance, validated_data):
        if 'email' in validated_data and validated_data['email'] != instance.email:
            validated_data['is_email_verified'] = False

        return super().update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    password1 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'password1',
            'first_name', 'last_name'
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({"password": _("Password fields didn't match.")})

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"message": _("This email already taken!")})

        # if not validate_domain_email(attrs['email']):
        #     raise serializers.ValidationError({"message": "Please enter the correct email!"})
        attrs.pop('password1')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ChangeUserPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(label=_("password"),
                                     style={"input_type": "password"}, validators=[validate_password], write_only=True)
    password1 = serializers.CharField(label=_("password1"), style={"input_type": "password"}, write_only=True)
    old_password = serializers.CharField(label=_("old password"), style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ("password", "password1", "old_password")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.context['request'].user

        if attrs['password'] == attrs['old_password']:
            raise serializers.ValidationError({
                "message": "You cannot change the password with the same current password"
            })

        elif attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({"message": "Password fields didn't match"})

        elif not user.check_password(attrs['old_password']):

            raise serializers.ValidationError({
                "message": _("Incorrect the current password, Please enter the correct current password")
            })

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
