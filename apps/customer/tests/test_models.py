import pytest
from apps.customer.tests.factories import WalletFactory


@pytest.mark.django_db
class TestWalletModel:
    def test_str(self):
        wallet = WalletFactory()

        assert str(wallet) == "Wallet with balance: $50"
