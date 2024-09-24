from django.contrib import admin

from .models import BankAccount, CashAccount, Account


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "tenant", "name", "balance", "accounttype")
    list_filter = ("tenant",)
    search_fields = ("name",)


@admin.register(CashAccount)
class CashAccountAdmin(admin.ModelAdmin):
    list_display = ("id", "tenant", "name", "balance")
    list_filter = ("tenant",)
    search_fields = ("name",)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "tenant", "name", "balance")
    list_filter = ("tenant",)
    search_fields = ("name",)
