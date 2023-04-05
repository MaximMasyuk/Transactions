from django.urls import path

from .views import TransactionListAPIView, TransactionDetailAPIView, transaction_list


urlpatterns = [
    path("", TransactionListAPIView.as_view(), name="transactions-list"),
    path("<int:pk>/", TransactionDetailAPIView.as_view(), name="transactions-detail"),
    path("<str:name_of_wallet>/", transaction_list),
]
