from django.urls import path

# , payments_received
from .views import (inventory, payments_made, purchase_add, purchase_detail,
                    purchase_index, supplier_detail)

purchase = [
    path("purchase/all/", purchase_index, name="purchase_index"),
    path("purchase/add/", purchase_add, name="purchase_add"),
    path("purchase/<int:id>/detail/", purchase_detail, name="purchase_detail"),
]

payments = [
    path("payments/made/", payments_made, name="payments_made"),
]

supplier = [
    path("supplier/<int:supplier_id>/detail/", supplier_detail, name="supplier_detail"),
]

stock = [
    path("inventory/", inventory, name="inventory"),
]

# adding to the urls
appname = "purchase"
urlpatterns = []
urlpatterns += purchase
urlpatterns += payments
urlpatterns += supplier
urlpatterns += stock
