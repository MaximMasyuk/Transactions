from rest_framework import generics
from .models import Wallet
from .serializers import WalletSerializer


# Create your views here.


class WalletListAPIView(generics.ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletCreateAPIView(generics.CreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WalletDetailAPIView(generics.RetrieveAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = "name"


class WalletDestroyAPIView(generics.DestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = "name"
