from django.urls import path

from .views import (
    WalletListAPIView,
    WalletCreateAPIView,
    WalletDetailAPIView,
    WalletDestroyAPIView,
    api_root,
)


urlpatterns = [
    path("", api_root),
    path("list/", WalletListAPIView.as_view(), name="wallet-list"),
    path("create/", WalletCreateAPIView.as_view(), name="wallet-create"),
    path("<str:name>/", WalletDetailAPIView.as_view(), name="wallet-detail"),
    path("delete/<str:name>/", WalletDestroyAPIView.as_view(), name="wallet-delete"),
]
