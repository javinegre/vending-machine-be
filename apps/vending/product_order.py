from apps.vending.models import VendingMachineSlot
from apps.customer.models import Customer


class OrderMissingResourceError(Exception):
    """Exception raised for missing resources (quantity or balance).

    Attributes:
        resource_type -- "quantity" or "stock"
    """

    def __init__(self, resource_type):
        self.resource_type = resource_type
        self.message = "Not enough {0}".format(resource_type)
        super().__init__(self.message)


class OrderPriceMismatchError(Exception):
    """Exception raised for price mismatch when purchasing"""

    def __init__(self):
        self.message = "Price mismatch"
        super().__init__(self.message)


class ProductOrder:
    def buy(self, customer_id, slot_id, price):

        slot = VendingMachineSlot.objects.get(id=slot_id)
        customer = Customer.objects.get(id=customer_id)

        if slot.quantity == 0:
            raise OrderMissingResourceError("stock")

        if str(slot.product.price) != price:
            raise OrderPriceMismatchError

        new_balance = customer.wallet.balance - slot.product.price

        if new_balance < 0:
            raise OrderMissingResourceError("balance")

        customer.wallet.balance = new_balance
        customer.wallet.save()

        return {"balance": new_balance}
