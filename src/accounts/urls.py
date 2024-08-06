from django.urls import path
from .views import accounts, create_accounts

urlpatterns = [
    path("accounts/all/", accounts, name="accounts_list"),
    path("accounts/create/", create_accounts, name="create"),
]
