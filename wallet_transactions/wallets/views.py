from rest_framework import generics
from .models import Wallet
from .serializers import WalletSerializer

# Create your views here.


class WalletCreateApiView(generics.ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
