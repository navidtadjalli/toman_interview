from datetime import timedelta
from decimal import Decimal
from http import HTTPStatus

from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response

from wallet import serializers
from wallet.models import Transaction, Wallet, LockedAmount


class CustomGenericAPIView(generics.GenericAPIView):
    def get_username_from_header(self, request) -> str:
        return request.META.get("HTTP_X_USERNAME")


class DepositAPIView(CustomGenericAPIView):
    serializer_class = serializers.DepositSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username: str = self.get_username_from_header(request)

        amount: Decimal = serializer.validated_data.pop('amount', Decimal(0.0))
        lock_time: int = serializer.validated_data.pop('lock_time', 0)

        wallet: Wallet
        wallet, _ = Wallet.objects.get_or_create(username=username)

        Transaction.objects.create(
            wallet_id=wallet.pk,
            amount=amount
        )

        LockedAmount.objects.create(
            wallet_id=wallet.pk,
            amount=amount,
            unlock_at=timezone.now() + timedelta(seconds=lock_time)
        )

        return Response({}, status=HTTPStatus.OK)


class WithdrawAPIView(CustomGenericAPIView):
    serializer_class = serializers.WithdrawSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username: str = self.get_username_from_header(request)

        return Response({}, status=HTTPStatus.OK)
