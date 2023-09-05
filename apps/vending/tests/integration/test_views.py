from decimal import Decimal
from unittest.mock import ANY
from uuid import uuid4

import factory
import pytest
from rest_framework import status
from apps.customer.tests.factories import CustomerFactory

from apps.vending.models import Product, VendingMachineSlot
from apps.vending.tests.factories import ProductFactory, VendingMachineSlotFactory


@pytest.fixture
def products_list() -> list[Product]:
    return [ProductFactory(id=uuid4(), name=f"Product {i}") for i in range(1, 13)]


@pytest.fixture
def slots_grid(products_list) -> list[VendingMachineSlot]:
    """returns a grid of slots of 4x3"""
    slots = []
    for row in range(1, 5):
        for column in range(1, 4):
            slot = VendingMachineSlotFactory(
                id=uuid4(), product=products_list.pop(), row=row, column=column, quantity=column-1
            )
            slots.append(slot)
    return slots


@pytest.mark.django_db
class TestListVendingMachineSlots:
    def test_list_slots_returns_expected_response(self, client, slots_grid):
        response = client.get("/slots/")

        expected_response = [
            [
                {
                    "id": ANY,
                    "quantity": 0,
                    "product": {"id": ANY, "name": "Product 12", "price": "10.40"},
                },
                {
                    "id": ANY,
                    "quantity": 1,
                    "product": {"id": ANY, "name": "Product 11", "price": "10.40"},
                },
                {
                    "id": ANY,
                    "quantity": 2,
                    "product": {"id": ANY, "name": "Product 10", "price": "10.40"},
                },
                None,
            ],
            [
                {
                    "id": ANY,
                    "quantity": 0,
                    "product": {"id": ANY, "name": "Product 9", "price": "10.40"},
                },
                {
                    "id": ANY,
                    "quantity": 1,
                    "product": {"id": ANY, "name": "Product 8", "price": "10.40"},
                },
                {
                    "id": ANY,
                    "quantity": 2,
                    "product": {"id": ANY, "name": "Product 7", "price": "10.40"},
                },
                None,
            ],
            [
                {
                    "id": ANY,
                    "quantity": 0,
                    "product": {"id": ANY, "name": "Product 6", "price": "10.40"},
                },
                {
                    "id": ANY,
                    "quantity": 1,
                    "product": {"id": ANY, "name": "Product 5", "price": "10.40"},
                },
                {
                    "id": ANY,
                    "quantity": 2,
                    "product": {"id": ANY, "name": "Product 4", "price": "10.40"},
                },
                None,
            ],
            [
                {
                    "id": ANY,
                    "quantity": 0,
                    "product": {"id": ANY, "name": "Product 3", "price": "10.40"},
                },
                {
                    "id": ANY,
                    "quantity": 1,
                    "product": {"id": ANY, "name": "Product 2", "price": "10.40"},
                },
                {
                    "id": ANY,
                    "quantity": 2,
                    "product": {"id": ANY, "name": "Product 1", "price": "10.40"},
                },
                None,
            ],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
        ]

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    def test_invalid_quantity_filter_returns_bad_request(self, client):
        response = client.get("/slots/?quantity=-1")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"quantity": [
            "Ensure this value is greater than or equal to 0."]}

    @pytest.mark.django_db
    def test_list_slots_returns_filtered_response(self, client, slots_grid):
        response = client.get("/slots/?quantity=1")

        expected_response = [
            [
                {
                    "id": ANY,
                    "quantity": 0,
                    "product": {"id": ANY, "name": "Product 12", "price": "10.40"},
                },
                {
                    "id": ANY,
                    "quantity": 1,
                    "product": {"id": ANY, "name": "Product 11", "price": "10.40"},
                },
                None,
                None,
            ],
            [
                {
                    "id": ANY,
                    "quantity": 0,
                    "product": {"id": ANY, "name": "Product 9", "price": "10.40"},
                },
                {
                    "id": ANY,
                    "quantity": 1,
                    "product": {"id": ANY, "name": "Product 8", "price": "10.40"},
                },
                None,
                None,
            ],
            [
                {
                    "id": ANY,
                    "quantity": 0,
                    "product": {"id": ANY, "name": "Product 6", "price": "10.40"},
                },
                {
                    "id": ANY,
                    "quantity": 1,
                    "product": {"id": ANY, "name": "Product 5", "price": "10.40"},
                },
                None,
                None,
            ],
            [
                {
                    "id": ANY,
                    "quantity": 0,
                    "product": {"id": ANY, "name": "Product 3", "price": "10.40"},
                },
                {
                    "id": ANY,
                    "quantity": 1,
                    "product": {"id": ANY, "name": "Product 2", "price": "10.40"},
                },
                None,
                None,
            ],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
        ]

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response


@pytest.mark.django_db
class TestProductOrder:
    def test_product_order_successful(self, client):
        test_slot = VendingMachineSlotFactory()
        test_customer = CustomerFactory()

        expected_response = {
            "balance": 39.6
        }

        response = client.post(
            "/buy/", data={"customer_id": test_customer.id, "slot_id": test_slot.id, "price": "10.40"})

        assert response.json() == expected_response

    def test_product_order_failed(self, client):
        test_slot = VendingMachineSlotFactory(quantity=0)
        test_customer = CustomerFactory()

        expected_response = {'error': 'Not enough stock'}

        response = client.post(
            "/buy/", data={"customer_id": test_customer.id, "slot_id": test_slot.id, "price": "10.40"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == expected_response
