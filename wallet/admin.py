from django.contrib import admin

from wallet.models import Wallet, Transaction


class WalletAdmin(admin.ModelAdmin):
    list_display = ("username",)
    search_fields = ("username",)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("wallet", "amount", "created_at",)
    search_fields = ("wallet__username",)
    readonly_fields = ("wallet", "amount", "created_at",)


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transaction, TransactionAdmin)
