from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

from .models import Wallet, COUNTOFWALLETYOUCANCREAT
from .serializers import WalletSerializer
from .permissions import IsOwner


# Create your views here.


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


@api_view(["GET", "POST"])
def wallet_create(request):
    """Create view creale for Wallet"""

    serializer = WalletSerializer(data=request.data)
    user = request.user
    count_wallet = Wallet.objects.filter(owner__username=user).count()
    if count_wallet >= COUNTOFWALLETYOUCANCREAT:
        return Response({"error": "You cannot create more than 5 wallets"})
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(("GET", "DELETE"))
def wallet_detail_delete(request, name_of_wallet: str):
    """Create view list for all transaction whose wallet number is name_of_wallet"""

    try:
        wallet = Wallet.objects.filter(owner__username=request.user).get(
            name=name_of_wallet
        )
    except Wallet.DoesNotExist:
        return Response({"error": "transaction does not exist"})
    if request.method == "GET":
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
    elif request.method == "DELETE":
        wallet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
