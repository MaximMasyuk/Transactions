from django.db.models import Q


from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Transaction, PAID
from .serialisers import TransactionSerializer
from .utils import (
    count_commission,
    check_low_balance,
    seve_wallet,
    count_transfer,
    check_currency,
)
from wallets.models import Wallet


@api_view(("GET", "DELETE"))
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def transaction_create(request):
    """Create view for transaction which create transaction and change the balance in wallets"""
    user = request.user
    serializer = TransactionSerializer(data=request.data)
    serializer.is_valid()
    if not serializer.is_valid():
        return Response({"error": "transaction does not exist"})

    wallet_sender = Wallet.objects.filter(owner__username=user).get(
        name=serializer.validated_data.get("sender")
    )
    wallet_receiver = Wallet.objects.get(name=serializer.validated_data.get("receiver"))

    commission = count_commission(user, wallet_receiver)
    com, transfer, sender_balanse = count_transfer(
        wallet_sender, serializer, commission
    )
    check_currency(wallet_sender, wallet_receiver, serializer, com)
    check_low_balance(sender_balanse, serializer, com)

    seve_wallet(wallet_sender, sender_balanse, wallet_receiver, transfer)

    serializer.save(transfer_amount=transfer, status=PAID, commission=com)
    return Response(serializer.data)
