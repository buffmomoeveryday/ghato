from django.conf import settings
from django.http import HttpResponseNotFound  # Import explicitly
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .models import TenantModel
from .utils import get_subdomain


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        request.tenant = None
        subdomain = get_subdomain(request)

        if subdomain:
            try:
                tenant = get_object_or_404(TenantModel, domain=subdomain)
                request.tenant = tenant
            except (TenantModel.DoesNotExist, Http404):
                if settings.DEBUG:
                    return HttpResponseNotFound("Tenant not found.")
                else:
                    return HttpResponseNotFound()
        else:
            # If the request is for the admin path, we don't assign a tenant
            if request.path.startswith("/admin/"):
                request.tenant = "Test Admin"

            else:
                if request.path.startswith("/unicorn/"):
                    response = self.get_response(request)
                    return response

                # Redirect to the registration page if there's no subdomain and tenant is not set
                if not request.tenant and not request.path == reverse("register"):
                    return redirect("register")

        response = self.get_response(request)
        return response


class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        pass
