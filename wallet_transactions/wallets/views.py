from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Wallet, COUNT_OF_WALLET_YOU_CAN_CREAT
from .serializers import WalletSerializer


@api_view(("GET",))
def wallet_list(request):
    """Create view list for all Wallet"""
    wallet = Wallet.objects.filter(owner__username=request.user)
    serializer = WalletSerializer(wallet, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def wallet_create(request):
    """Create view create for Wallet"""
    serializer = WalletSerializer(data=request.data)
    user = request.user
    count_wallet = Wallet.objects.filter(owner__username=user).count()
    if count_wallet >= COUNT_OF_WALLET_YOU_CAN_CREAT:
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
        return Response({"error": "wallet does not exist"})
    if request.method == "GET":
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
    elif request.method == "DELETE":
        wallet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
