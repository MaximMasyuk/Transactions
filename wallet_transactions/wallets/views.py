from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Wallet
from .serializers import WalletSerializer
from .permissions import IsOwner


# Create your views here.


class WalletListAPIView(generics.ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = (IsOwner,)


class WalletCreateAPIView(generics.CreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WalletDetailAPIView(generics.RetrieveAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = "name"
    permission_classes = (IsOwner,)


class WalletDestroyAPIView(generics.DestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = "name"
    permission_classes = (IsOwner,)


@api_view(["GET"])
def api_root(request, format=None):
    return Response({"wallets": reverse("wallet-list", request=request, format=format)})
