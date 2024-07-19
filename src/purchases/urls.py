from django.urls import path


from .views import purchase_detail, purchase_index, purchase_add, supplier_detail
from .views import payments_made

# , payments_received
from .views import inventory


purchase = [
    path("purchase/all/", purchase_index, name="purchase_index"),
    path("purchase/add/", purchase_add, name="purchase_add"),
    path("purchase/<int:id>/detail/", purchase_detail, name="purchase_detail"),
]

payments = [
    path("payments/made/", payments_made, name="payments_made"),
    # path("payments/received/", payments_received, name="payments_received"),
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
