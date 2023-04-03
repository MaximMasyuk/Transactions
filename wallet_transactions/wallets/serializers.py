from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
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
