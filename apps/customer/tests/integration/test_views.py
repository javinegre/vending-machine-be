from decimal import Decimal
from unittest.mock import ANY
from uuid import uuid4

import factory
import pytest
from rest_framework import status

from apps.customer.models import Customer
from apps.customer.tests.factories import WalletFactory, CustomerFactory


@pytest.fixture
def customers() -> list[Customer]:
    """returns a list of customers"""
    return [
        CustomerFactory(id=uuid4(), user_name="user-1",
                        password="password-1", wallet=WalletFactory(id=uuid4())),
        CustomerFactory(id=uuid4(), user_name="user-2",
                        password="password-2", wallet=WalletFactory(id=uuid4())),
        CustomerFactory(id=uuid4(), user_name="user-3",
                        password="password-3", wallet=WalletFactory(id=uuid4())),
    ]


@pytest.mark.django_db
class TestLogin:
    def test_successful_login(self, client, customers):
        data = {
            "user_name": "user-2",
            "password": "password-2",
        }

        response = client.post("/login/", data=data)

        expected_response = {
            "id": ANY,
            "user_name": "user-2",
            "profile": {
                "first_name": "Miquel",
                "last_name": "Montoro"
            },
            "wallet": {
                "id": ANY,
                "balance": "10.00"
            }
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    def test_unsuccessful_login_if_wrong_user_name(self, client, customers):
        data = {
            "user_name": "user-1",
            "password": "password-2",
        }

        response = client.post("/login/", data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_unsuccessful_login_if_wrong_password(self, client, customers):
        data = {
            "user_name": "user-2",
            "password": "password-3",
        }

        response = client.post("/login/", data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_malformed_login_payload_returns_400(self, client, customers):
        data = {}

        response = client.post("/login/", data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
