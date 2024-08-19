from django.conf import settings
from django.http import HttpResponseNotFound, Http404  # Import explicitly
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.utils.cache import patch_vary_headers
from django.core.cache import cache
import hashlib
from icecream import ic


from .models import TenantModel
from .utils import get_subdomain, get_host_name


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Generate cache key based on the user
        cache_key = self.get_cache_key(request)
        tenant = cache.get(cache_key)

        if tenant:
            request.tenant = tenant
        else:
            request.tenant = None
            subdomain = get_subdomain(request)

            if subdomain:
                try:
                    tenant = get_object_or_404(TenantModel, domain=subdomain)
                    request.tenant = tenant
                    # Cache the tenant for the user
                    cache.set(
                        cache_key, tenant, timeout=60 * 15
                    )  # Cache for 15 minutes
                except (TenantModel.DoesNotExist, Http404):
                    if settings.DEBUG:
                        domain: str = request.get_host().split(".")[1]
                        response = HttpResponsePermanentRedirect(
                            f"http://{domain}/register"
                        )
                    else:
                        response = HttpResponseNotFound()
                    patch_vary_headers(response, ["Cookie"])
                    return response
            else:
                if request.path.startswith("/admin/"):
                    request.tenant = "Test Admin"
                else:
                    if request.path.startswith("/unicorn/"):
                        response = self.get_response(request)
                        patch_vary_headers(response, ["Cookie"])
                        return response

                    if not request.tenant and not request.path == reverse("register"):
                        return redirect("register")

        response = self.get_response(request)
        patch_vary_headers(response, ["Cookie"])
        return response

    def get_cache_key(self, request):
        """
        Generate a cache key based on the user and request URL.
        """
        cookie_hash = hashlib.md5(str(request.COOKIES).encode("utf-8")).hexdigest()
        return f"tenant_cache_{cookie_hash}"


class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        pass
