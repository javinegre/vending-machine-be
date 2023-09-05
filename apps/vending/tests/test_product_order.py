import pytest

from apps.customer.tests.factories import CustomerFactory, WalletFactory
from apps.vending.product_order import OrderMissingResourceError, OrderPriceMismatchError, ProductOrder
from apps.vending.tests.factories import VendingMachineSlotFactory


@pytest.mark.django_db
class TestProductOrder:

    def test_buy_success(self):
        test_slot = VendingMachineSlotFactory()
        test_customer = CustomerFactory()

        order = ProductOrder()
        result = order.buy(test_customer.id, test_slot.id, "10.40")

        assert isinstance(result, dict)

    def test_buy_fail_not_enough_balance(self):
        test_slot = VendingMachineSlotFactory()
        test_customer = CustomerFactory(wallet=WalletFactory(balance=0.01))

        expected_error_message = "Not enough balance"

        order = ProductOrder()

        result = ""
        # with pytest.raises(OrderMissingResourceError):
        try:
            order.buy(test_customer.id, test_slot.id, "10.40")
        except OrderMissingResourceError as ex:
            result = ex.message

        assert result == expected_error_message

    def test_buy_fail_not_enough_stock(self):
        test_slot = VendingMachineSlotFactory(quantity=0)
        test_customer = CustomerFactory()

        expected_error_message = "Not enough stock"

        order = ProductOrder()

        result = ""
        try:
            order.buy(test_customer.id, test_slot.id, "10.40")
        except OrderMissingResourceError as ex:
            result = ex.message

        assert result == expected_error_message

    def test_buy_fail_price_mismatch(self):
        test_slot = VendingMachineSlotFactory()
        test_customer = CustomerFactory()

        expected_error_message = "Price mismatch"

        order = ProductOrder()

        result = ""
        try:
            order.buy(test_customer.id, test_slot.id, "40.10")
        except OrderPriceMismatchError as ex:
            result = ex.message

        assert result == expected_error_message
