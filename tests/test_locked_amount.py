import decimal
from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from wallet.models import Transaction, Wallet, LockedAmount


class LockedAmountModelTestCase(TestCase):
    def setUp(self):
        pass

    def test_if_locked_amount_model_has_required_fields(self):
        locked_amount: LockedAmount = LockedAmount()

        self.assertTrue(hasattr(locked_amount, "wallet_id"))
        self.assertTrue(hasattr(locked_amount, "amount"))
        self.assertTrue(hasattr(locked_amount, "unlock_at"))

    def test_str_function(self):
        wallet: Wallet = Wallet.objects.create(username="test")
        now: datetime = timezone.now()
        locked_amount: LockedAmount = LockedAmount.objects.create(
            wallet_id=wallet.pk,
            amount="123.12",
            unlock_at=now
        )

        self.assertEqual(str(locked_amount), f"123.12 of test is locked until {now}")
