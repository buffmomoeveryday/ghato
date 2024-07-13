from django.contrib import admin

from .models import (Customer, Product, PurchaseInovice, PurchaseItem,
                     Supplier, UnitOfMeasurements)

# Register your models here.

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(PurchaseItem)
admin.site.register(PurchaseInovice)
admin.site.register(Supplier)
admin.site.register(UnitOfMeasurements)
