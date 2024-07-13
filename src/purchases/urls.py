from django.urls import path


from .views import purchase_detail, purchase_index, purchase_add

appname = "purchase"
urlpatterns = [
    path("purchase/", purchase_index, name="purchase_index"),
    path("purchase/add/", purchase_add, name="purchase_add"),
    path("purchase/<int:id>/detail", purchase_detail, name="purchase_detail"),
]
