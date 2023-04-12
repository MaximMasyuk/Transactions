from .models import ZERO_COMMISION, FAILED
import decimal
from rest_framework.response import Response

NO_COMMISSION = 0
BANK_COMMISSION = 0.1


def check_currency(wallet_sender, wallet_receiver, serializer, com):
    """Check currency for receiver and sender"""
    if wallet_sender.currency != wallet_receiver.currency:
        serializer.save(status=FAILED, commission=com)
        return Response({"ERROR": "Transacrion faild"})


def count_commission(user, wallet_receiver):
    """Get commission"""

    commission = NO_COMMISSION if wallet_receiver.owner == user else BANK_COMMISSION

    return commission


def count_transfer(wallet_sender, serializer, commission):
    """Count transfer attribute"""
    if commission == NO_COMMISSION:
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
    if sender_balanse < NO_COMMISSION:
        serializer.save(status=FAILED, commission=com)
        return Response({"ERROR": "Transaction faild"})


def seve_wallet(wallet_sender, sender_balanse, wallet_receiver, transfer):
    """The function for save Wallet"""
    wallet_sender.balance = sender_balanse
    wallet_receiver.balance = wallet_receiver.balance + transfer

    wallet_sender.save(update_fields=["balance"])
    wallet_receiver.save(update_fields=["balance"])
