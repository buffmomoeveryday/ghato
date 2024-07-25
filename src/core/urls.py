import debug_toolbar
from django.contrib import admin
from django.urls import include, path

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
]


urlpatterns += auth_urls
