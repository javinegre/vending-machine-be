from django.db import models
from decimal import Decimal
from uuid import uuid4
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):
    class Meta:
        db_table = "product"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=4, decimal_places=2, validators=[
                                MinValueValidator(Decimal("0.00"))])
    created_at = models.DateTimeField(auto_now_add=True)


class VendingMachineSlot(models.Model):
    class Meta:
        db_table = "vending_machine_slot"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)])
    row = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)])
    column = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)])
