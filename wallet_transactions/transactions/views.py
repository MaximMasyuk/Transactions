import decimal
from django.db.models import Q

from rest_framework import views, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Transaction, ZEROCOMMISION, PAID, FAILED
from .serialisers import TransactionSerializer

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
        return Response({"error": "transaction does not exist"})


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
    try:
        wallet_sender = Wallet.objects.filter(owner__username=user).get(
            name=serializer.validated_data.get("sender")
        )
        wallet_recever = Wallet.objects.get(
            name=serializer.validated_data.get("receiver")
        )

    except Wallet.DoesNotExist:
        return Response({"error": "the wallet does not exist"})

    if wallet_sender.owner == wallet_recever.owner:
        com = ZEROCOMMISION
        transfer = serializer.validated_data.get("transfer_amount")

    else:
        com = serializer.validated_data.get("transfer_amount") * decimal.Decimal(0.1)
        transfer = serializer.validated_data.get("transfer_amount") - com

    if wallet_sender.currency != wallet_recever.currency:
        serializer.save(status=FAILED, commission=com)
        return Response({"ERROR": "Transacrion faild"})

    sender_balanse = wallet_sender.balance - transfer

    if sender_balanse > 0:
        serializer.save(status=FAILED, commission=com)
        return Response({"ERROR": "Transacrion faild"})

    wallet_sender.balance = sender_balanse
    wallet_recever.balance = wallet_recever.balance + transfer

    wallet_sender.save(update_fields=["balance"])
    wallet_recever.save(update_fields=["balance"])

    serializer.save(transfer_amount=transfer, status=PAID, commission=com)
    return Response(serializer.data)


class TransactionView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        print(serializer.data)
