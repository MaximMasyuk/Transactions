from rest_framework import serializers

from .models import Wallet


class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)


class WalletSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(read_only=True)

    class Meta:
        model = Wallet
        fields = [
            "id",
            "name",
            "type_of_wallet",
            "currency",
            "balance",
            "owner",
            "created_on",
            "modified_on",
        ]
