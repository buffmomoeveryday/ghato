import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from .views import analytics

urlpatterns = []


auth_urls = [
    path(
        "",
        analytics,
        name="analytics",
    ),
]


urlpatterns += auth_urls
