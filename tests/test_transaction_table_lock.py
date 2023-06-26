import concurrent.futures
import json
from decimal import Decimal
from http import HTTPStatus
from typing import Optional, Callable

from django.db import connections
from django.test import TransactionTestCase
from django.urls import reverse

from tests.custom_api_test_case import CustomAPITestCase
from wallet.models import Wallet


class TransactionLockTestCase(TransactionTestCase):
    GET_METHOD_TYPE: str = "GET"
    POST_METHOD_TYPE: str = "POST"

    DEFAULT_USERNAME = "username"

    def call_endpoint(self, url: str, method: str, data: Optional[dict] = None, headers: Optional[dict] = None):
        callable_method: Callable = self.client.get

        if method == self.GET_METHOD_TYPE:
            callable_method = self.client.get
        if method == self.POST_METHOD_TYPE:
            callable_method = self.client.post

        callable_arguments = {
            "path": url,
            "content_type": "application/json",
        }

        if data:
            callable_arguments["data"] = json.dumps(data)

        if not headers:
            headers = {}

        headers["X_USERNAME"] = self.DEFAULT_USERNAME
        callable_arguments["headers"] = headers

        return callable_method(**callable_arguments)

    def call_endpoint_with_get(self, url: str, data: Optional[dict] = None, headers: Optional[dict] = None):
        return self.call_endpoint(url, self.GET_METHOD_TYPE, data=data, headers=headers)

    def call_endpoint_with_post(self, url: str, data: dict = None, headers: Optional[dict] = None):
        return self.call_endpoint(url, self.POST_METHOD_TYPE, data=data, headers=headers)

    def setUp(self):
        self.deposit_url = reverse("deposit")
        self.withdraw_url = reverse("withdraw")

    def on_done(self, future):
        connections.close_all()

    def call_deposit(self, amount: int, lock_time: int):
        self.call_endpoint_with_post(self.deposit_url, data={"amount": amount, "lock_time": lock_time})

    def call_withdraw(self, amount: int):
        return self.call_endpoint_with_post(self.withdraw_url, data={"amount": amount})

    def test_racing_condition(self):
        self.call_deposit(100, 0)
        withdrawal_statuses: list[int] = []

        def withdraw_50():
            response = self.call_withdraw(50)
            withdrawal_statuses.append(response.status_code)

        num_threads = 5
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for _ in range(num_threads):
                future = executor.submit(withdraw_50)
                future.add_done_callback(self.on_done)

        wallet_balance: Decimal = Wallet.objects.get().balance
        self.assertGreaterEqual(wallet_balance, Decimal(0))
        self.assertEqual(wallet_balance, Decimal(0))
        self.assertEqual(len(list(filter(lambda x: x == HTTPStatus.NO_CONTENT, withdrawal_statuses))), 2)
