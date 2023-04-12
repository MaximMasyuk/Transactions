from .models import ZERO_COMMISION, FAILED
import decimal
from rest_framework.response import Response

ZERO_BALANCE = 0.00
BANK_COMMISSION = 0.1


def count_commission(wallet_sender, wallet_recever, serializer):
    """Count commssion for Transaction"""
    if wallet_sender.owner == wallet_recever.owner:
        commission = ZERO_COMMISION
        transfer = serializer.validated_data.get("transfer_amount")

    else:
        commission = serializer.validated_data.get("transfer_amount") * decimal.Decimal(
            BANK_COMMISSION
        )
        transfer = serializer.validated_data.get("transfer_amount") - commission

    sender_balanse = wallet_sender.balance - transfer
    return commission, transfer, sender_balanse


def check_low_balance(sender_balanse, serializer, com):
    """Check the balance wallet"""
    if sender_balanse < ZERO_BALANCE:
        serializer.save(status=FAILED, commission=com)
        return Response({"ERROR": "Transaction faild"})


def seve_wallet(wallet_sender, sender_balanse, wallet_recever, transfer):
    """The function for save Wallet"""
    wallet_sender.balance = sender_balanse
    wallet_recever.balance = wallet_recever.balance + transfer

    wallet_sender.save(update_fields=["balance"])
    wallet_recever.save(update_fields=["balance"])
