from _decimal import Decimal
from datetime import datetime
from uuid import uuid4

import pytest
import factory

from apps.customer.models import Customer, Wallet


class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wallet

    id = uuid4()
    balance = Decimal(50.0)


@pytest.mark.django_db
def test_wallet_creation():
    test_wallet = WalletFactory(
        balance=Decimal("15.50"))

    stored_wallet = Wallet.objects.get(id=test_wallet.id)

    assert stored_wallet == test_wallet
    assert stored_wallet.balance == Decimal("15.50")


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    id = uuid4()
    user_name = "miquel"
    password = "h05714-P1l0t35"
    first_name = "Miquel"
    last_name = "Montoro"
    wallet = factory.SubFactory(WalletFactory)
    created_at = datetime(2023, 5, 30, 12)
    updated_at = datetime(2023, 5, 30, 23)


@pytest.mark.django_db
def test_customer_creation():
    test_wallet = WalletFactory()

    test_customer = CustomerFactory(
        user_name="Test", password="p455w0Rd", first_name="Maikel", wallet=test_wallet)

    stored_customer = Customer.objects.get(id=test_customer.id)

    assert stored_customer == test_customer
    assert stored_customer.user_name == "Test"
    assert stored_customer.password == "p455w0Rd"
    assert stored_customer.first_name == "Maikel"
    assert stored_customer.last_name == "Montoro"
    assert stored_customer.wallet == test_wallet
    assert stored_customer.wallet.balance == Decimal(50.0)
