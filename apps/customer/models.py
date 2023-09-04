from django.db import models
from decimal import Decimal
from uuid import uuid4
from django.core.validators import MinValueValidator


class Wallet(models.Model):
    class Meta:
        db_table = "wallet"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    balance = models.DecimalField(max_digits=6, decimal_places=2, validators=[
        MinValueValidator(Decimal("0.00"))])


class Customer(models.Model):
    class Meta:
        db_table = "customer"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    wallet = models.ForeignKey("Wallet", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
