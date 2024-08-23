from django.conf import settings
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme

from .models import TenantModel


def get_host_name(request):
    try:
        if hasattr(request, "get_host") and callable(getattr(request, "get_host")):
            return request.get_host().split(":")[0].lower()
    except Exception as e:
        print(f"Exception occurred in get_host_name: {e}")
    return None


def get_subdomain(request):
    hostname = get_host_name(request=request)
    if hostname is None:
        return None

    parts = hostname.split(".")
    if len(parts) < 2:
        return None
    return parts[0]


def get_tenant(request):
    subdomain = get_subdomain(request=request)

    if subdomain is None:
        return None

    try:
        return TenantModel.objects.filter(domain=subdomain).first()
    except Exception as e:
        print(f"Exception occurred in get_tenant: {e}")
        return None


def redirect_after_login(request):
    next_url = request.GET.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_url)
    return redirect(settings.TENANT_LOGIN_REDIRECT)
