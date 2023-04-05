from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Transaction
from .serialisers import TransactionSerializer
from .permission import IsOwnerTransaction


class TransactionDetailAPIView(generics.RetrieveAPIView):
    """Create view with detail for certain Transaction"""

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (IsOwnerTransaction,)


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
