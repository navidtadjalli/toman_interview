from datetime import timedelta
from decimal import Decimal
from http import HTTPStatus

from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response

from wallet import serializers
from wallet.models import Transaction, Wallet


class CustomGenericAPIView(generics.GenericAPIView):
    def get_username_from_header(self, request) -> str:
        return request.META.get("HTTP_X_USERNAME")

    def get_wallet(self, request) -> Wallet:
        wallet, _ = Wallet.objects.get_or_create(username=self.get_username_from_header(request))
        return wallet


class DepositAPIView(CustomGenericAPIView):
    serializer_class = serializers.DepositSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount: Decimal = serializer.validated_data.pop('amount', Decimal(0.0))
        lock_time: int = serializer.validated_data.pop('lock_time', 0)

        wallet: Wallet = self.get_wallet(request)

        Transaction.objects.create(
            wallet_id=wallet.pk,
            amount=amount,
            available_at=timezone.now() + timedelta(seconds=lock_time)
        )

        return Response(status=HTTPStatus.NO_CONTENT)


class WithdrawAPIView(CustomGenericAPIView):
    serializer_class = serializers.WithdrawSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wallet: Wallet = self.get_wallet(request)

        # wallet.balance

        return Response({}, status=HTTPStatus.OK)
