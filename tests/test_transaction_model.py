from django.test import TestCase

from wallet.models import Transaction, Wallet


class TransactionModelTestCase(TestCase):
    def setUp(self):
        pass

    def test_if_transaction_model_has_required_fields(self):
        transaction: Transaction = Transaction()

        self.assertTrue(hasattr(transaction, "wallet_id"))
        self.assertTrue(hasattr(transaction, "amount"))
        self.assertTrue(hasattr(transaction, "created_at"))

    def test_str_function(self):
        wallet: Wallet = Wallet.objects.create(username="test")
        transaction: Transaction = Transaction.objects.create(
            wallet_id=wallet.pk,
            amount="123.12"
        )

        self.assertEqual(str(transaction), f"Transaction for test wallet at {transaction.created_at}")

    def test_for_negative_amount(self):
        wallet: Wallet = Wallet.objects.create(username="test")
        transaction: Transaction = Transaction.objects.create(
            wallet_id=wallet.pk,
            amount="-123.12"
        )

        self.assertEqual(str(transaction), f"Transaction for test wallet at {transaction.created_at}")
