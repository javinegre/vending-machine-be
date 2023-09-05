from django.contrib import admin
from apps.vending.models import Product, VendingMachineSlot


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "created_at", "updated_at"]
    ordering = ["-created_at"]


admin.site.register(Product, ProductAdmin)


class VendingMachineSlotAdmin(admin.ModelAdmin):
    list_display = ["row", "column", "product", "quantity"]
    ordering = ["row", "column"]


admin.site.register(VendingMachineSlot, VendingMachineSlotAdmin)
