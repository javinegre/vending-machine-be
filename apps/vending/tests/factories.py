from _decimal import Decimal
from datetime import datetime
from uuid import uuid4

import pytest
from factory.django import DjangoModelFactory

from apps.vending.models import Product, VendingMachineSlot


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    id = uuid4()
    name = "Snickers Bar"
    price = Decimal("10.40")
    created_at = datetime(2023, 5, 30, 12)
    updated_at = datetime(2023, 5, 30, 23)

# This annotation (see more in section 3) is required because factories
# inheriting from DjangoModelFactory will be stored in the db.
# You can prevent this by calling the .build() method instead of
# the constructor (ProductFactory.build(name="Heidi chocolate"))


@pytest.mark.django_db
def test_product_creation():
    test_product = ProductFactory(
        name="Heidi chocolate", price=Decimal("5.32"))

    stored_product = Product.objects.get(id=test_product.id)

    assert stored_product == test_product
    assert stored_product.price == Decimal("5.32")
    assert stored_product.name == "Heidi chocolate"


class VendingMachineSlotFactory(DjangoModelFactory):
    class Meta:
        model = VendingMachineSlot

    id = uuid4()
    quantity = 2
    row = 1
    column = 1


@pytest.mark.django_db
def test_vending_machine_slot_creation():
    test_product = ProductFactory()
    test_vending_machine_slot = VendingMachineSlotFactory(product=test_product,
                                                          quantity=3, row=4, column=5)

    stored_vending_machine_slot = VendingMachineSlot.objects.get(
        id=test_vending_machine_slot.id)

    assert stored_vending_machine_slot == test_vending_machine_slot
    assert stored_vending_machine_slot.product == test_product
    assert stored_vending_machine_slot.quantity == 3
    assert stored_vending_machine_slot.row == 4
    assert stored_vending_machine_slot.column == 5
