from django.urls import path

from .views import sales_add, sales_all, sales_detail, sales_invoice
from .views import customer_all, customer_detail
from .views import payments_received

sales = [
    path("sales/all/", sales_all, name="sales_list"),
    path("sales/<int:sales_id>/detail/", sales_detail, name="sales_detail"),
    path("sales/add/", sales_add, name="sales_add"),
    path("sales/<int:sales_id>/invoice", sales_invoice, name="sales_invoice"),
]


customers = [
    path("customer/all/", customer_all, name="customer_all"),
    path("customer/<int:customer_id>/detail/", customer_detail, name="customer_detail"),
]


payments = [
    path("payments/received/", payments_received, name="payments_received"),
]


appname = "sales"
urlpatterns = []
urlpatterns += sales
urlpatterns += payments
urlpatterns += customers
