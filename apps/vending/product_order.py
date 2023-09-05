from apps.vending.models import VendingMachineSlot
from apps.customer.models import Customer


class ProductOrder:
    def buy(self, customer_id, slot_id):

        slot = VendingMachineSlot.objects.get(id=slot_id)
        customer = Customer.objects.get(id=customer_id)

        # TODO raise exception
        if slot.quantity == 0:
            return False

        new_balance = customer.wallet.balance - slot.product.price

        # TODO raise exception
        if new_balance < 0:
            return False

        customer.wallet.balance = new_balance
        customer.wallet.save()

        return {"balance": new_balance}
