from django.db import models
from decimal import Decimal
from uuid import uuid4
from django.core.validators import MinValueValidator


class Product(models.Model):
    class Meta:
        db_table = "product"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=4, decimal_places=2, validators=[
                                MinValueValidator(Decimal("0.00"))])
    created_at = models.DateTimeField(auto_now_add=True)
