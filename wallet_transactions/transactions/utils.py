from .models import ZERO_COMMISION, FAILED
import decimal
from rest_framework.response import Response

ZERO_BALANCE = 0.00
NO_COMMISSION = 0
BANK_COMMISSION = 0.1


def count_commission(user, wallet_recever):
    """Get commission"""

    commission = NO_COMMISSION if wallet_recever.owner == user else BANK_COMMISSION

    return commission


def count_transfer(wallet_sender, serializer, commission):
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
    if sender_balanse < ZERO_BALANCE:
        serializer.save(status=FAILED, commission=com)
        return Response({"ERROR": "Transacrion faild"})


def seve_wallet(wallet_sender, sender_balanse, wallet_recever, transfer):
    wallet_sender.balance = sender_balanse
    wallet_recever.balance = wallet_recever.balance + transfer

    wallet_sender.save(update_fields=["balance"])
    wallet_recever.save(update_fields=["balance"])
