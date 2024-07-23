from django.contrib import admin

from .models import Customer, PaymentReceived, Sales, SalesInvoice, SalesItem

# Register your models here.

admin.site.register(Sales)
admin.site.register(Customer)
admin.site.register(PaymentReceived)
admin.site.register(SalesInvoice)


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


admin.site.register(SalesItem, SalesItemAdmin)
