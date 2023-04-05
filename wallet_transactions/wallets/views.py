from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Wallet, COUNTOFWALLETYOUCANCREAT
from .serializers import WalletSerializer
from .permissions import IsOwner


# Create your views here.


class WalletCreateAPIView(generics.CreateAPIView):
    """Create view for create the wallet"""

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def post(self, request, *args, **kwargs):
        """Method wich chec count of wallet at the user and if count
        is 5 user can't create more wallet"""
        user = request.user
        count_wallet = Wallet.objects.filter(owner__username=user).count()

        if count_wallet >= COUNTOFWALLETYOUCANCREAT:
            return Response({"error": "You cannot create more than 5 wallets"})

        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Method wich add login user for wallet"""
        serializer.save(owner=self.request.user)


class WalletDetailAPIView(generics.RetrieveAPIView):
    """Create view with detail for certain Wallet"""

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = "name"
    permission_classes = (IsOwner,)


class WalletDestroyAPIView(generics.DestroyAPIView):
    """Create view wich destroy certain Wallet"""

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = "name"
    permission_classes = (IsOwner,)


@api_view(("GET",))
def wallet_list(request):
    """Create view list for all Wallet"""
    wallet = Wallet.objects.filter(owner__username=request.user)
    serializer = WalletSerializer(wallet, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def api_root(request, format=None):
    """Create view for front page"""
    return Response(
        {
            "wallets": reverse("wallet_list", request=request, format=format),
            "transactions": reverse(
                "transactions_list", request=request, format=format
            ),
        },
    )
