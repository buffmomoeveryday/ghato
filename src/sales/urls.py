from django.urls import path

from .views import sales_add, sales_all, sales_detail, sales_invoice, payment
from .views import customer_all, customer_detail
from .views import payments_received, payment_successfull

from sales.components.payment_received_component import PaymentReceivedComponentView

sales = [
    path("sales/all/", sales_all, name="sales_list"),
    path("sales/<int:sales_id>/detail/", sales_detail, name="sales_detail"),
    path("sales/add/", sales_add, name="sales_add"),
    path("sales/<int:sales_id>/invoice", sales_invoice, name="sales_invoice"),
    path("payment/<int:sales_id>/", payment, name="payment"),
    path("payment/successfull/", payment_successfull, name="payment_successfull"),
]


customers = [
    path("customer/all/", customer_all, name="customer_all"),
    path("customer/<int:customer_id>/detail/", customer_detail, name="customer_detail"),
]


payments = [
    path(
        "payments/received/",
        payments_received,
        name="payments_received",
    ),
    path(
        "payments/received/create/",
        PaymentReceivedComponentView.as_view(),
        name="payments_received_create",
    ),
]


appname = "sales"
urlpatterns = []
urlpatterns += sales
urlpatterns += payments
urlpatterns += customers
