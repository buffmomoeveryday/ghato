from django.urls import path
from .views import accounts, create_accounts

urlpatterns = [
    path("accounts/", accounts, name="accounts"),
    path("accounts/create/", create_accounts, name="create"),
]
