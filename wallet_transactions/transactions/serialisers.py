from rest_framework import serializers
from .models import Transaction
from wallets.models import Wallet


class TransactionSerializer(serializers.ModelSerializer):
    """Serialize Transaction model"""

    class Meta:
        model = Transaction
        fields = [
            "id",
            "sender",
            "receiver",
            "transfer_amount",
            "commission",
            "status",
            "timestamp",
        ]

    def validate_title(self, value):
        """Verifies valid transaction data"""
        request = self.context.get("request")
        user = request.user
        try:
            sender_wallet = Wallet.objects.filter(owner__username=user).get(
                name="sender"
            )
            receiver_wallet = Wallet.objects.get(name="receiver")
        except Wallet.DoesNotExist:
            raise serializers.ValidationError(f"{value} the wallet does not exist")

        if sender_wallet.currency != receiver_wallet.currency:
            raise serializers.ValidationError("Currency is not normal")
        return value
