from django.urls import path

from .views import (
    transaction_list,
    TransactionDetailAPIView,
    transaction_list_for_name,
)


urlpatterns = [
    path("", transaction_list, name="transactions_list"),
    path("<int:pk>/", TransactionDetailAPIView.as_view(), name="transactions_detail"),
    path("<str:name_of_wallet>/", transaction_list_for_name),
]
