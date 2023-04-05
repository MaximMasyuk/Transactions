from django.urls import path

from .views import (
    wallet_list,
    wallet_detail_delete,
    api_root,
    wallet_create,
)


urlpatterns = [
    path("", api_root),
    path("list/", wallet_list, name="wallet_list"),
    path("create/", wallet_create, name="wallet_create"),
    path("<str:name_of_wallet>/", wallet_detail_delete, name="wallet_detail_delete"),
]
