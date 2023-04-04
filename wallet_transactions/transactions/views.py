from django.db.models import Q

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Transaction
from .serialisers import TransactionSerializer


# Create your views here.


class TransactionListAPIView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionDetailAPIView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


@api_view(("GET",))
def transaction_list(request, name_of_wallet):
    transaction = Transaction.objects.filter(
        Q(sender__name=name_of_wallet) | Q(receiver__name=name_of_wallet)
    )
    serializer = TransactionSerializer(transaction, many=True)
    if not transaction:
        return Response({"error": "transaction does not exist"})
    return Response(serializer.data)
