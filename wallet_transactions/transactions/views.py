from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Transaction
from .serialisers import TransactionSerializer
from .permission import IsOwnerTransaction


# Create your views here.


class TransactionListAPIView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (IsOwnerTransaction,)


class TransactionDetailAPIView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (IsOwnerTransaction,)


@api_view(("GET",))
def transaction_list(request, name_of_wallet: str):
    print(request.user.id)
    transaction = Transaction.objects.filter(
        Q(sender__owner=request.user.id) | Q(receiver__owner=request.user.id)
    ).filter(Q(sender__name=name_of_wallet) | Q(receiver__name=name_of_wallet))
    print(request)
    serializer = TransactionSerializer(transaction, many=True)
    if not transaction:
        return Response({"error": "transaction does not exist"})
    return Response(serializer.data)
