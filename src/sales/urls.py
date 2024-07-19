from django.urls import path
from .views import sales_add

sales = [
    path("sales/add/", sales_add, name="sales_add"),
]

# adding to the urls
appname = "sales"
urlpatterns = []
urlpatterns += sales
