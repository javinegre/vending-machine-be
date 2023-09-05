from decimal import Decimal
import pytest
from apps.customer.tests.factories import CustomerFactory, WalletFactory
from apps.customer.wallet_actions import WalletActions


@pytest.mark.django_db
class TestWalletAddMoney:

    def test_add_money_success(self):
        test_customer = CustomerFactory(
            wallet=WalletFactory(balance=Decimal("20.00")))

        walletActions = WalletActions()
        result = walletActions.addMoney(test_customer.id, Decimal("10.00"))

        assert result == {"balance": 30.00}


@pytest.mark.django_db
class TestWalletRefund:

    def test_refund_success(self):
        test_customer = CustomerFactory()

        walletActions = WalletActions()
        result = walletActions.refund(test_customer.id)

        assert result == {"balance": 0.00}
