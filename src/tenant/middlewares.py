from typing import Any
from django.conf import settings
from django.http import (
    HttpResponseNotFound,
    Http404,
    JsonResponse,
    HttpResponseForbidden,
)
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.urls import reverse
from django.utils.cache import patch_vary_headers
from django.core.cache import cache
import hashlib
from icecream import ic

from .models import TenantModel
from .utils import get_subdomain


from django.http import HttpResponse


class APIKeyMiddleware:
    def __init__(self, get_response, **kwargs):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/"):
            if "HTTP_X_API_KEY" not in request.META:
                # Instead of returning HttpResponse, set an attribute on the request
                request.api_key_valid = False
            else:
                request.api_key_valid = True
        else:
            request.api_key_valid = True  # Non-API requests are considered valid

        # Always continue to the next middleware
        response = self.get_response(request)
        return response


class TenantMiddleware:
    """
    Middleware to handle tenant-specific logic based on the subdomain of the request.
    Caches tenant information for improved performance and manages user redirection
    based on tenant existence and application state.
    """

    def __init__(self, get_response):
        """
        Initializes the middleware with the get_response function.

        Args:
            get_response (callable): The next middleware or view in the stack.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Processes each request to determine the tenant based on the subdomain.

        The tenant is retrieved from the cache if available, or queried from the database
        if not. Handles redirection and response generation based on the presence or
        absence of the tenant.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The HTTP response, which may be a redirect, a 404 error,
            or a normal response with tenant-specific content.
        """

        # Check for X-API-Key in the request headers

        if "HTTP_X_API_KEY" in request.META and request.path.startswith("/api/"):
            return self.get_response(request)

        if hasattr(request, "api_key_valid") and not request.api_key_valid:
            return HttpResponse("No API Key", status=401)

        # Generate cache key based on the user's cookies
        cache_key = self.get_cache_key(request)
        tenant = cache.get(cache_key)

        ic(cache_key)
        ic(tenant)

        if tenant:
            # Assign the tenant to the request if found in the cache
            request.tenant = tenant
        else:
            request.tenant = None
            subdomain = get_subdomain(request)

            if subdomain:
                try:
                    # Attempt to retrieve tenant based on subdomain
                    tenant = get_object_or_404(TenantModel, domain=subdomain)
                    request.tenant = tenant
                    cache.set(cache_key, tenant, timeout=60 * 15)

                except (TenantModel.DoesNotExist, Http404):
                    if settings.DEBUG:
                        if request.path.startswith("/api/"):
                            response = JsonResponse({"not found": "not found"})
                        else:
                            domain = request.get_host().split(".")[1]
                            response = HttpResponsePermanentRedirect(
                                f"http://{domain}/register"
                            )
                    else:
                        response = HttpResponseNotFound()

                    patch_vary_headers(response, ["Cookie"])
                    return response
            else:
                # Special handling for admin paths
                if request.path.startswith("/admin/"):
                    request.tenant = "Test Admin"
                else:
                    # Special handling for unicorn paths
                    if request.path.startswith("/unicorn/"):
                        response = self.get_response(request)
                        patch_vary_headers(response, ["Cookie"])
                        return response

                    # Redirect to register if no tenant and not already on register page
                    if not request.tenant and request.path != reverse("register"):
                        return redirect("register")

        response = self.get_response(request)
        patch_vary_headers(response, ["Cookie"])
        return response

    def get_cache_key(self, request) -> str:
        """
        Generates a unique cache key for storing and retrieving tenant information.

        The cache key is based on a hashed version of the request's cookies to ensure
        uniqueness per user.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            str: The generated cache key.
        """
        # Ensure cookies are processed as a string in a consistent way
        cookies_string = str(sorted(request.COOKIES.items()))
        cookie_hash = hashlib.md5(cookies_string.encode("utf-8")).hexdigest()
        return f"tenant_cache_{cookie_hash}"
