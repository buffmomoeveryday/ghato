from django.contrib import admin

from .models import Customer, Sales, SalesInvoice, SalesItem, PaymentReceived


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "address",
    )
    list_filter = ("tenant", "created_at", "updated_at", "created_by")
    date_hierarchy = "created_at"


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "customer",
        "total_amount",
        "returned",
    )
    list_filter = (
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "customer",
        "returned",
    )
    date_hierarchy = "created_at"


@admin.register(SalesInvoice)
class SalesInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "sales",
        "billing_address",
        "total_amount",
        "payment_status",
    )
    list_filter = (
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "sales",
    )
    date_hierarchy = "created_at"


@admin.register(SalesItem)
class SalesItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "sales",
        "product",
        "quantity",
        "price",
        "stock_snapshot",
        "vat",
        "vat_amount",
    )
    list_filter = (
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "sales",
        "product",
    )
    date_hierarchy = "created_at"


@admin.register(PaymentReceived)
class PaymentReceivedAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "amount",
        "payment_method",
        "payment_date",
        "transaction_id",
        "customer",
    )
    list_filter = (
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "payment_date",
        "customer",
    )
    date_hierarchy = "created_at"
