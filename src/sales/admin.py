from django.contrib import admin

from .models import Customer, PaymentReceived, Sales, SalesInvoice, SalesItem

# Register your models here.


class SalesItemAdmin(admin.ModelAdmin):
    list_display = [
        "sales",
        "product",
        "quantity",
        "price",
        "total",
        "vat",
        "vat_amount",
    ]

    @admin.display(empty_value="???")
    def total(self, obj):
        return obj.quantity * obj.price


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "phone_number", "address"]


class SalesAdmin(admin.ModelAdmin):
    list_display = ["customer", "total_amount"]


class SalesInvoiceAdmin(admin.ModelAdmin):
    list_display = ["sales", "billing_address", "total_amount", "payment_status"]


class PaymentReceivedAdmin(admin.ModelAdmin):
    list_display = [
        "amount",
        "payment_method",
        "payment_date",
        "transaction_id",
        "customer",
    ]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(SalesItem, SalesItemAdmin)
admin.site.register(Sales, SalesAdmin)
admin.site.register(SalesInvoice, SalesInvoiceAdmin)
admin.site.register(PaymentReceived, PaymentReceivedAdmin)
