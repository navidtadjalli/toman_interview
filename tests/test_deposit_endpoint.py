from http import HTTPStatus

from django.urls import reverse

from tests.custom_api_test_case import CustomAPITestCase


class DepositAPITestCase(CustomAPITestCase):
    def setUp(self):
        self.url = reverse("deposit")

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
