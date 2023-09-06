import pytest

from apps.vending.tests.factories import ProductFactory, VendingMachineSlotFactory


@pytest.mark.django_db
class TestProductModel:
    def test_str(self):
        product = ProductFactory()

        assert str(product) == "Snickers Bar ($10.40)"


@pytest.mark.django_db
class TestVendingMachineSlotModel:
    def test_str(self):
        vendingMachine = VendingMachineSlotFactory()

        assert str(vendingMachine) == "1-1 > Snickers Bar ($10.40)"
