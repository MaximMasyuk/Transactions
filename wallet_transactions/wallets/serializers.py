import decimal
from rest_framework import serializers, validators

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    """Serialize Wallet model"""

    class Meta:
        balance = serializers.DecimalField(max_digits=10, decimal_places=2)
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

        def validate(self, attrs):
            balance = attrs.get("balance")
            if balance < decimal.Decimal(0.0):
                raise validators.ValidationError(
                    {"message": "Balance can't be lower than 0"}
                )
