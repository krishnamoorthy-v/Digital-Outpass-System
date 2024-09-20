from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PasswordResetModel, LoginModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"]
        )
        return user


# class LoginSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(required=True)
#     password = serializers.CharField(required=True)


class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetModel
        fields = "__all__"


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginModel
        fields = "__all__"


def isValidRole(value):
    roles = ["warden", "student", "security", "department"]
    value = value.lower()
    if value not in roles:
        raise serializers.ValidationError("Invalid role")
    else:
        return value


class SignupSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(required=True, validators=[isValidRole])

    class Meta:
        model = LoginModel
        fields = "__all__"
