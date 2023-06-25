from unittest import TestCase

from wallet.models import Wallet


class WalletModelTestCase(TestCase):
    def setUp(self):
        pass

    def test_if_wallet_model_has_required_fields(self):
        wallet: Wallet = Wallet()

        self.assertTrue(hasattr(wallet, "username"))
        self.assertTrue(hasattr(wallet, "transactions"))

    def test_str_function(self):
        wallet: Wallet = Wallet(
            username="Test"
        )
        wallet.save()

        self.assertEqual(str(wallet), wallet.username)
