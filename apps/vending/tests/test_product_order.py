from uuid import uuid4
import pytest

from apps.customer.tests.factories import CustomerFactory
from apps.vending.product_order import ProductOrder
from apps.vending.tests.factories import VendingMachineSlotFactory


@pytest.mark.django_db
class TestProductOrder:

    def test_buy(self):
        test_slot = VendingMachineSlotFactory(id=uuid4())
        test_customer = CustomerFactory()

        order = ProductOrder()
        result = order.buy(test_customer.id, test_slot.id)

        assert isinstance(result, dict)
