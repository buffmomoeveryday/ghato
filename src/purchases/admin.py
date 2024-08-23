from django.contrib import admin

from .models import (
    PaymentMade,
    Product,
    PurchaseInvoice,
    PurchaseItem,
    Supplier,
    UnitOfMeasurements,
    StockMovement,
    PurchaseReturn,
    PurchaseReturnItem,
)

# Register your models here.

admin.site.register(Product)

admin.site.register(PurchaseItem)
admin.site.register(PurchaseInvoice)

admin.site.register(Supplier)
admin.site.register(UnitOfMeasurements)
admin.site.register(StockMovement)

admin.site.register(PaymentMade)
admin.site.register(PurchaseReturnItem)
admin.site.register(PurchaseReturn)
