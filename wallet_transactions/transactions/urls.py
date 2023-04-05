from django.urls import path

from .views import (
    transaction_list,
    transaction_detail_delete,
    transaction_list_for_name,
)


urlpatterns = [
    path("", transaction_list, name="transactions_list"),
    path("<int:pk>/", transaction_detail_delete, name="transactions_detail_delete"),
    path("<str:name_of_wallet>/", transaction_list_for_name),
]
