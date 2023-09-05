from django.contrib import admin
from apps.customer.models import Wallet, Customer


class WalletAdmin(admin.ModelAdmin):
    list_display = ["id", "balance"]


admin.site.register(Wallet, WalletAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["user_name", "first_name", "last_name",
                    "wallet", "created_at", "updated_at"]
    ordering = ["-created_at"]


admin.site.register(Customer, CustomerAdmin)
