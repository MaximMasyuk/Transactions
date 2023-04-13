from rest_framework import serializers

from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """Serialize User model for register"""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        """The function which check validate of data and create user"""
        user = User.objects.create_user(
            validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serialize User model"""

    class Meta:
        model = User
        fields = "__all__"
