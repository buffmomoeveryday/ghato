from django.http import HttpResponsePermanentRedirect
from django.urls import path, reverse_lazy
from fbv.views import redirect_view

from .views import dashboard_index, assistant, chat

appname = "dashboard"


def redirect_to_dashboard(request):
    return HttpResponsePermanentRedirect(redirect_to=reverse_lazy("dashboard_index"))


urlpatterns = [
    path("", redirect_to_dashboard),
    path("dashboard/", dashboard_index, name="dashboard_index"),
    path("assistant/", assistant, name="assistant"),
    path("chat/", chat, name="chat"),
]
