import debug_toolbar
from django.contrib import admin
from django.urls import include, path

from purchases.api import purchase_api, supplier_api, accounts


urlpatterns = [
    path("admin/", admin.site.urls),
    path("unicorn/", include("django_unicorn.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
]


auth_urls = [
    path("", include("dashboard.urls")),
    path("", include("users.urls")),
    path("", include("purchases.urls")),
    path("", include("sales.urls")),
    path("", include("accounts.urls")),
    path("analytics/", include("analytics.urls")),
]

api_urls = [
    path("api/purchase/", purchase_api.urls),
    path("api/supplier/", supplier_api.urls),
    path("api/accounts/", accounts.urls),
]


urlpatterns += auth_urls
urlpatterns += api_urls
