from decimal import Decimal
from http import HTTPStatus

from rest_framework import generics
from rest_framework.response import Response

from wallet import serializers
from wallet.models import Transaction, Wallet


class CustomGenericAPIView(generics.GenericAPIView):
    def get_username_from_header(self, request) -> str:
        return request.META.get("HTTP_X_USERNAME")


class DepositAPIView(CustomGenericAPIView):
    serializer_class = serializers.DepositSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username: str = self.get_username_from_header(request)

        wallet: Wallet
        wallet, _ = Wallet.objects.get_or_create(username=username)

        Transaction.objects.create(
            wallet_id=wallet.pk,
            amount=serializer.validated_data.pop('amount', Decimal(0.0))
        )

        return Response({}, status=HTTPStatus.OK)
