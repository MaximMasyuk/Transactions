from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import RegisterApi


urlpatterns = [
    path("", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("veryfy/", TokenVerifyView.as_view(), name="token_veryfyveryfy"),
    path("register/", RegisterApi.as_view(), name="token_register"),
]
