from django.contrib import admin

from .models import (PaymentMade, Product, PurchaseInovice, PurchaseItem,
                     Supplier, UnitOfMeasurements)

# Register your models here.

admin.site.register(Product)
admin.site.register(PurchaseItem)
admin.site.register(PurchaseInovice)
admin.site.register(Supplier)
admin.site.register(UnitOfMeasurements)

admin.site.register(PaymentMade)
