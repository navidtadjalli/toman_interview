from django.urls import path

from wallet import views

urlpatterns = [
    path("api/deposit", views.DepositAPIView.as_view(), name="deposit"),
    path("api/withdraw", views.WithdrawAPIView.as_view(), name="withdraw"),
]