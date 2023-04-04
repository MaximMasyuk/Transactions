from django.urls import path

from .views import TransactionListAPIView, transaction_list


urlpatterns = [
    path("", TransactionListAPIView.as_view(), name="transactions-list"),
    path("<int:pk>/", TransactionListAPIView.as_view(), name="transactions-list"),
    path("<str:name_of_wallet>/", transaction_list),
]
