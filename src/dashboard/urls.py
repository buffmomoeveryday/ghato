from django.http import HttpResponsePermanentRedirect
from django.urls import path, reverse_lazy

from .views import dashboard_index

appname = "dashboard"


def redirect_to_dashboard(request):
    return HttpResponsePermanentRedirect(reverse_lazy("dashboard_index"))


urlpatterns = [
    path("", redirect_to_dashboard, name="dashboard_redirect"),
    path("dashboard/", dashboard_index, name="dashboard_index"),
]
