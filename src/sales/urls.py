from django.urls import path
from .views import sales_add, sales_list

sales = [
    path("sales/add/", sales_add, name="sales_add"),
    path("sales/list/", sales_list, name="sales_list"),
]

# adding to the urls
appname = "sales"
urlpatterns = []
urlpatterns += sales
