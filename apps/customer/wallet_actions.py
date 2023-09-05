from decimal import Decimal
from apps.customer.models import Customer


class WalletActions:
    def addMoney(self, customer_id, amount):

        customer = Customer.objects.get(id=customer_id)

        new_balance = customer.wallet.balance + Decimal(amount)

        customer.wallet.balance = new_balance
        customer.wallet.save()

        return {"balance": new_balance}

    def refund(self, customer_id):

        customer = Customer.objects.get(id=customer_id)

        customer.wallet.balance = 0
        customer.wallet.save()

        return {"balance": 0}
