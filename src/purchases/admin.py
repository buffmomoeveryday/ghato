from django.contrib import admin
from .models import (
    UnitOfMeasurements,
    Product,
    StockMovement,
    PaymentMade,
    Supplier,
    PurchaseInvoice,
    PurchaseItem,
    PurchaseReturn,
    PurchaseReturnItem,
)


@admin.register(UnitOfMeasurements)
class UnitOfMeasurementsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "name",
        "field",
    )
    list_filter = ("tenant", "created_at", "updated_at", "created_by")
    search_fields = ("name",)
    date_hierarchy = "created_at"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "name",
        "uom",
        "sku",
        "stock_quantity",
        "opening_stock",
    )
    list_filter = ("tenant", "created_at", "updated_at", "created_by", "uom")
    search_fields = ("name",)
    date_hierarchy = "created_at"


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "product",
        "movement_type",
        "quantity",
        "date",
        "description",
    )
    list_filter = (
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "product",
        "date",
    )
    date_hierarchy = "created_at"


@admin.register(PaymentMade)
class PaymentMadeAdmin(admin.ModelAdmin):
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
        "supplier",
    )
    list_filter = (
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "payment_date",
        "supplier",
    )
    date_hierarchy = "created_at"


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "name",
        "contact_person",
        "email",
        "phone_number",
        "address",
    )
    list_filter = ("tenant", "created_at", "updated_at", "created_by")
    search_fields = ("name",)
    date_hierarchy = "created_at"


@admin.register(PurchaseInvoice)
class PurchaseInvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "supplier",
        "invoice_number",
        "purchase_date",
        "total_amount",
        "received_date",
        "order_date",
        "returned",
    )
    list_filter = (
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "supplier",
        "purchase_date",
        "received_date",
        "order_date",
        "returned",
    )
    date_hierarchy = "created_at"


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "purchase",
        "product",
        "quantity",
        "price",
    )
    list_filter = (
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "purchase",
        "product",
    )
    date_hierarchy = "created_at"


@admin.register(PurchaseReturn)
class PurchaseReturnAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "purchase_invoice",
        "return_date",
        "total_amount",
    )
    list_filter = (
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "purchase_invoice",
        "return_date",
    )
    date_hierarchy = "created_at"


@admin.register(PurchaseReturnItem)
class PurchaseReturnItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "purchase_return",
        "product",
        "quantity",
        "price",
    )
    list_filter = (
        "tenant",
        "created_at",
        "updated_at",
        "created_by",
        "purchase_return",
        "product",
    )
    date_hierarchy = "created_at"
