from functools import wraps
from typing import List

from ninja import NinjaAPI
from ninja.security import APIKeyHeader

from icecream import ic

from tenant.models import TenantModel
from tenant.utils import get_subdomain
from purchases.models import PurchaseInvoice, PurchaseItem
from tenant.models import TenantModel


def require_htmx(view_func):
    def wrapper(request, *args, **kwargs):
        if request.headers.get("HX-Request"):
            pass
        else:
            raise
        response = view_func(request, *args, **kwargs)
        # code to be executed after the view
        return response

    return wrapper


def api_exempt(view_func):
    """
    Decorator used to skip the Tenatnt middleware in ninja api.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        setattr(request, "_skip_ninja_api", True)
        return view_func(request, *args, **kwargs)

    return _wrapped_view


# api key headers


class ApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        try:
            if key:
                subdomain = get_subdomain(request)
                return TenantModel.objects.get(api_key=key, domain=subdomain)
            else:
                pass

        except TenantModel.DoesNotExist:
            pass
