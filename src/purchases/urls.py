from django.urls import path
from .api import purchase_api

from sales.components.payment_received_component import PaymentReceivedComponentView

from .views import (
    inventory,
    payments_made,
    payments_made_create,
    purchase_add,
    purchase_detail,
    purchase_index,
    supplier_detail,
    settings,
    product_analytics,
    stock_movement,
    supplier_list,
    supplier_edit,
    purchase_return,
)

api = []


purchase = [
    path("purchase/all/", purchase_index, name="purchase_index"),
    path("purchase/add/", purchase_add, name="purchase_add"),
    path("purchase/<int:id>/detail/", purchase_detail, name="purchase_detail"),
    path("purchase/<int:purchase_id>/return/", purchase_return, name="purchase_return"),
]

payments = [
    path("payments/made/", payments_made, name="payments_made"),
    path("payments/made/create/", payments_made_create, name="payments_made_create"),
]

supplier = [
    path("supplier/<int:supplier_id>/detail/", supplier_detail, name="supplier_detail"),
    path("supplier/all/", supplier_list, name="supplier_list"),
    path("supplier/<int:supplier_id>/edit/", supplier_edit, name="supplier_edit"),
]

stock = [
    path("inventory/", inventory, name="inventory"),
    path("inventory/movement/", stock_movement, name="stock_movement"),
]

setting = [
    path("purchase/settings/", settings, name="purchase_settings"),
]

product = [
    path(
        "product/<int:product_id>/analytics/",
        product_analytics,
        name="product_analytics",
    ),
]

# adding to the urls
appname = "purchase"
urlpatterns = []

urlpatterns += purchase
urlpatterns += payments
urlpatterns += supplier
urlpatterns += stock
urlpatterns += setting
urlpatterns += product

urlpatterns += api
