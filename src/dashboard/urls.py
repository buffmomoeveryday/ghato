from django.urls import path
from django.http import HttpResponsePermanentRedirect
from .views import dashboard_index
from django.urls import reverse_lazy

appname = "dashboard"


def redirect_to_dashboard(request):
    return HttpResponsePermanentRedirect(reverse_lazy("dashboard_index"))


urlpatterns = [
    path("", redirect_to_dashboard, name="dashboard_redirect"),
    path("dashboard/", dashboard_index, name="dashboard_index"),
]
