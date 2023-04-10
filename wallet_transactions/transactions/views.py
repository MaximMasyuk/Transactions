from django.db.models import Q


from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Transaction, PAID, FAILED
from .serialisers import TransactionSerializer
from .utils import count_commission, check_low_balance, seve_wallet

from wallets.models import Wallet


@api_view(("GET", "DELETE"))
def transaction_detail_delete(request, pk: int):
    """Create view list for all transaction whose transaction pk is pk"""

    try:
        transaction = Transaction.objects.filter(
            Q(sender__owner=request.user.id) | Q(receiver__owner=request.user.id)
        ).get(pk=pk)
    except Transaction.DoesNotExist:
        return Response({"error": "transaction does not exist"})
    if request.method == "GET":
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
    elif request.method == "DELETE":
        transaction.delete()
        return Response({"Status": "transaction was delete"})


@api_view(("GET",))
def transaction_list(request):
    """Create view list for all Transaction"""
    transaction = Transaction.objects.filter(
        Q(sender__owner=request.user.id) | Q(receiver__owner=request.user.id)
    )
    serializer = TransactionSerializer(transaction, many=True)
    if not transaction:
        return Response({"error": "transaction does not exist"})
    return Response(serializer.data)


@api_view(("GET",))
def transaction_list_for_name(request, name_of_wallet: str):
    """Create view list for all transaction whose wallet number is name_of_wallet"""
    transaction = Transaction.objects.filter(
        Q(sender__owner=request.user.id) | Q(receiver__owner=request.user.id)
    ).filter(Q(sender__name=name_of_wallet) | Q(receiver__name=name_of_wallet))
    serializer = TransactionSerializer(transaction, many=True)
    if not transaction:
        return Response({"error": "transaction does not exist"})
    return Response(serializer.data)


@api_view(["POST"])
def transaction_create(request):
    """Create view for transaction which create transaction and chenge the balance in wallets"""
    user = request.user
    serializer = TransactionSerializer(data=request.data)
    serializer.is_valid()
    if not serializer.is_valid():
        return Response({"error": "faild"})

    wallet_sender = Wallet.objects.filter(owner__username=user).get(
        name=serializer.validated_data.get("sender")
    )
    wallet_recever = Wallet.objects.get(name=serializer.validated_data.get("receiver"))

    com, transfer, sender_balanse = count_commission(
        wallet_sender, wallet_recever, serializer
    )

    if wallet_sender.currency != wallet_recever.currency:
        serializer.save(status=FAILED, commission=com)
        return Response({"ERROR": "Transacrion faild"})

    check_low_balance(sender_balanse, serializer, com)

    seve_wallet(wallet_sender, sender_balanse, wallet_recever, transfer)

    serializer.save(transfer_amount=transfer, status=PAID, commission=com)
    return Response(serializer.data)
