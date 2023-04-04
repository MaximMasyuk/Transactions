from django.urls import path

from .views import TransactionListAPIView


urlpatterns = [
    path(
        "list/",
        TransactionListAPIView.as_view(),
        name="transactions-list",
    ),
    path(
        "detail/<int:pk>/",
        TransactionListAPIView.as_view(),
        name="transactions-list",
    ),
]
