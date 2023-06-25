from decimal import Decimal
from http import HTTPStatus

from django.urls import reverse

from tests.custom_api_test_case import CustomAPITestCase
from wallet.models import Wallet


class DepositAPITestCase(CustomAPITestCase):
    def setUp(self):
        self.url = reverse("deposit")

        self.wallet = Wallet.objects.create(username=self.DEFAULT_USERNAME)

    def test_if_deposit_endpoint_exists(self):
        self.assertNotEqual(self.call_endpoint_with_get(self.url).status_code, HTTPStatus.NOT_FOUND)

    def test_if_deposit_endpoint_is_post(self):
        self.assertEqual(self.call_endpoint_with_get(self.url).status_code, HTTPStatus.METHOD_NOT_ALLOWED)
        self.assertNotEqual(self.call_endpoint_with_post(self.url).status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_if_deposit_checks_that_required_fields_are_sent_in_body(self):
        response = self.call_endpoint_with_post(self.url)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("amount", response.data)
        self.assertIn("lock_time", response.data)

    def test_deposit_response_status_is_200_if_input_is_correct(self):
        response = self.call_endpoint_with_post(self.url,
                                                data={"amount": "9.9", "lock_time": 123})

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_deposit_validates_amount_field_is_number(self):
        response = self.call_endpoint_with_post(self.url,
                                                data={"amount": "amount", "lock_time": 123})

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("amount", response.data)

    def test_deposit_validates_amount_field_maximum_digits(self):
        response = self.call_endpoint_with_post(self.url,
                                                data={"amount": "999999999999999", "lock_time": 123})

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("amount", response.data)

    def test_deposit_validates_amount_field_maximum_decimal_digits(self):
        response = self.call_endpoint_with_post(self.url,
                                                data={"amount": "9.999", "lock_time": 123})

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("amount", response.data)

    def test_deposit_validates_amount_field_is_more_than_zero(self):
        response = self.call_endpoint_with_post(self.url,
                                                data={"amount": "-9.9", "lock_time": 123})

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("amount", response.data)

    def test_deposit_validates_lock_time_field_is_number(self):
        response = self.call_endpoint_with_post(self.url,
                                                data={"amount": "9.9", "lock_time": "lock_time"})

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("lock_time", response.data)

    def test_deposit_validates_lock_time_field_is_more_than_equal_zero(self):
        response = self.call_endpoint_with_post(self.url,
                                                data={"amount": "9.9", "lock_time": -1})

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("lock_time", response.data)

    def test_deposit_accepts_lock_time_being_zero(self):
        response = self.call_endpoint_with_post(self.url,
                                                data={"amount": "9.9", "lock_time": 0})

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_deposit_validates_lock_time_field_does_not_accepts_float(self):
        response = self.call_endpoint_with_post(self.url,
                                                data={"amount": "9.9", "lock_time": 0.5})

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("lock_time", response.data)

    def test_deposit_inserts_a_transaction(self):
        response = self.call_endpoint_with_post(self.url,
                                                data={"amount": "9.9", "lock_time": 1})

        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertTrue(self.wallet.transactions.exists())
        self.assertEqual(self.wallet.transactions.get().amount, Decimal("9.9"))

    def test_deposit_affects_lock_time(self):
        response = self.call_endpoint_with_post(self.url,
                                                data={"amount": "9.9", "lock_time": 1})

        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertTrue(self.wallet.transactions.exists())
        self.assertEqual(self.wallet.transactions.get().amount, Decimal("9.9"))
