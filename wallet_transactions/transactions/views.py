from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics

from .models import Transaction
from .serialisers import TransactionSerializer

# Create your views here.


class TransactionListAPIView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["sender__name", "receiver__name"]

    # def get_queryset(self):
    #     serializer = TransactionSerializer(data=self.request.data)
    #     if serializer.is_valid():
    #         print(Response(serializer.data))
    #     print(Response(serializer.data))

    #     return super().get_queryset()


class TransactionDetailAPIView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
