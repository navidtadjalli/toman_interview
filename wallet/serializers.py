from decimal import Decimal

from rest_framework import serializers


class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        required=True,
        allow_null=False,
        max_digits=14,
        decimal_places=2,
        min_value=Decimal(0.01)
    )
    lock_time = serializers.IntegerField(
        required=True,
        allow_null=False,
        min_value=0
    )


class WithdrawSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        required=True,
        allow_null=False,
        max_digits=14,
        decimal_places=2,
        min_value=Decimal(0.01)
    )