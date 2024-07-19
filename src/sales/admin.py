from django.contrib import admin
from .models import Customer, PaymentReceived, Sales, SalesInvoice, SalesItem

# Register your models here.


admin.site.register(SalesItem)
admin.site.register(Sales)
admin.site.register(Customer)
admin.site.register(PaymentReceived)
admin.site.register(SalesInvoice)
