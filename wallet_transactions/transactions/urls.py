from django.urls import path

from .views import (
    transaction_list,
    transaction_detail_delete,
    transaction_list_for_name,
    transaction_create,
)


urlpatterns = [
    path("", transaction_list, name="transactions_list"),
    path("create/", transaction_create, name="transaction_create"),
    path("<int:pk>/", transaction_detail_delete, name="transactions_detail_delete"),
    path(
        "<str:name_of_wallet>/",
        transaction_list_for_name,
        name="transaction_list_for_name",
    ),
]
