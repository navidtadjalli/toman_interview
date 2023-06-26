from decimal import Decimal
from http import HTTPStatus

from django.urls import reverse

from tests.custom_api_test_case import CustomAPITestCase
from toman_interview import error_messages
from wallet.models import Wallet


class WithdrawAPITestCase(CustomAPITestCase):
    def setUp(self):
        self.deposit_url = reverse("deposit")
        self.url = reverse("withdraw")

        self.wallet = Wallet.objects.create(username=self.DEFAULT_USERNAME)

    def test_if_withdraw_endpoint_exists(self):
        self.assertNotEqual(self.call_endpoint_with_get(self.url).status_code, HTTPStatus.NOT_FOUND)

    def test_if_withdraw_endpoint_is_post(self):
        self.assertEqual(self.call_endpoint_with_get(self.url).status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertNotEqual(self.call_endpoint_with_post(self.url).status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_if_withdraw_checks_that_required_fields_are_sent_in_body(self):
        response = self.call_endpoint_with_post(self.url)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("amount", response.data)

    def test_withdraw_validates_amount_field_is_number(self):
        response = self.call_endpoint_with_post(self.url,
                                                data={"amount": "amount"})

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("amount", response.data)

    def test_withdraw_validates_amount_field_maximum_digits(self):
        response = self.call_endpoint_with_post(self.url,
                                                data={"amount": "999999999999999"})

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("amount", response.data)

    def test_withdraw_validates_amount_field_maximum_decimal_digits(self):
        response = self.call_endpoint_with_post(self.url,
                                                data={"amount": "9.999"})

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("amount", response.data)

    def test_withdraw_validates_amount_field_is_more_than_zero(self):
        response = self.call_endpoint_with_post(self.url,
                                                data={"amount": "-9.9"})

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("amount", response.data)

    def test_withdraw_checks_wallet_balance(self):
        response = self.call_endpoint_with_post(self.url,
                                                data={"amount": "9.9"})

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, error_messages.INSUFFICIENT_BALANCE_ERROR_MESSAGE)

    def test_withdraw_checks_only_available_balance_balance(self):
        self.call_endpoint_with_post(self.deposit_url, data={"amount": "9.9", "lock_time": 10})
        response = self.call_endpoint_with_post(self.url, data={"amount": "1.9"})

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, error_messages.INSUFFICIENT_BALANCE_ERROR_MESSAGE)

    def test_withdraw_inserts_a_transaction(self):
        self.call_endpoint_with_post(self.deposit_url, data={"amount": "100.0", "lock_time": 0})
        response = self.call_endpoint_with_post(self.url, data={"amount": "10.0"})

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

        self.assertTrue(self.wallet.transactions.exists())
        self.assertEqual(self.wallet.transactions.last().amount, Decimal("-10.0"))
