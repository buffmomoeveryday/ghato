from django.urls import path

from .views import sales_add, sales_all, sales_detail, payments_received

sales = [
    path("sales/all/", sales_all, name="sales_list"),
    path("sales/<int:sales_id>/detail/", sales_detail, name="sales_detail"),
    path("sales/add/", sales_add, name="sales_add"),
]


payments = [
    path("payments/received/", payments_received, name="payments_received"),
]


# adding to the urls
appname = "sales"
urlpatterns = []
urlpatterns += sales
urlpatterns += payments
