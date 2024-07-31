from django.urls import path

# , payments_received
from .views import (
    inventory,
    payments_made,
    purchase_add,
    purchase_detail,
    purchase_index,
    supplier_detail,
    settings,
    product_analytics,
    stock_movement,
)

purchase = [
    path("purchase/all/", purchase_index, name="purchase_index"),
    path("purchase/add/", purchase_add, name="purchase_add"),
    path("purchase/<int:id>/detail/", purchase_detail, name="purchase_detail"),
]

payments = [
    path(
        "payments/made/",
        payments_made,
        name="payments_made",
    ),
]

supplier = [
    path(
        "supplier/<int:supplier_id>/detail/",
        supplier_detail,
        name="supplier_detail",
    ),
]

stock = [
    path(
        "inventory/",
        inventory,
        name="inventory",
    ),
    path(
        "inventory/movement/",
        stock_movement,
        name="stock_movement",
    ),
]

setting = [
    path(
        "purchase/settings/",
        settings,
        name="purchase_settings",
    ),
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
