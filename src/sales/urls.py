from django.urls import path
from .views import sales_add, sales_all, sales_detail

sales = [
    path("sales/all/", sales_all, name="sales_list"),
    path("sales/<int:sales_id>/detail/", sales_detail, name="sales_detail"),
    path("sales/add/", sales_add, name="sales_add"),
]

# adding to the urls
appname = "sales"
urlpatterns = []
urlpatterns += sales
