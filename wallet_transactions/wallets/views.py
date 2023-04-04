from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Wallet
from .serializers import WalletSerializer
from .permissions import IsOwner


# Create your views here.

COUNTOFWALLETYOUCANCREAT = 5


class WalletListAPIView(generics.ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = (IsOwner,)


class WalletCreateAPIView(generics.CreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        count_wallet = Wallet.objects.filter(owner__username=user).count()

        if count_wallet >= COUNTOFWALLETYOUCANCREAT:
            return Response({"error": "You cannot create more than 5 wallets"})

        return super().post(request, *args, **kwargs)

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
    return Response(
        {
            "wallets": reverse("wallet-list", request=request, format=format),
            "transactions": reverse(
                "transactions-list", request=request, format=format
            ),
        },
    )
