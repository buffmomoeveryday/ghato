from typing import List

from ninja import NinjaAPI
from ninja.security import APIKeyHeader
from ninja.pagination import paginate, LimitOffsetPagination
from ninja import Query
from ninja.decorators import decorate_view

from icecream import ic
from django.views.decorators.cache import cache_page

from tenant.models import TenantModel
from tenant.utils import get_subdomain
from core.utils import ApiKey

from accounts import models
from sales.models import PaymentReceived
from .models import PurchaseInvoice, PurchaseItem, Supplier, PaymentMade
from .schemas import (
    PurchaseInvoiceOutSchema,
    PurchaseInvoiceCreateSchema,
    PurchaseInvoiceFilterSchema,
    SupplierOutSchema,
    PurchaseInvoiceDetailOutSchema,
)

from django.shortcuts import get_object_or_404, get_list_or_404

purchase_api = NinjaAPI(auth=ApiKey(), urls_namespace="purchase api", openapi_url=None)
supplier_api = NinjaAPI(auth=ApiKey(), urls_namespace="supplier api", openapi_url=None)
accounts = NinjaAPI(auth=ApiKey(), openapi_url=None)


@purchase_api.get("/all/", response={200: List[PurchaseInvoiceOutSchema]})
@decorate_view(cache_page(40 * 10))
@paginate(LimitOffsetPagination)
def purchase_all(request, filters: PurchaseInvoiceFilterSchema = Query(None)):
    purchases = PurchaseInvoice.objects.filter(tenant=request.auth)
    filtered_purchases = filters.filter(purchases)
    return filtered_purchases


@purchase_api.get("/get/{purchase_id}/", response={200: PurchaseInvoiceDetailOutSchema})
def purchase_get(request, purchase_id):
    purchase = (
        PurchaseInvoice.objects.prefetch_related(
            "items__product__uom",
        )
        .filter(tenant=request.auth)
        .get(id=purchase_id)
    )
    return purchase


@purchase_api.get(
    "/supplier/{supplier_id}/", response={200: List[PurchaseInvoiceDetailOutSchema]}
)
@paginate(LimitOffsetPagination)
@decorate_view(cache_page(60 * 15))
def supplier_purchases(
    request, supplier_id, filters: PurchaseInvoiceFilterSchema = Query(None)
):
    purchases = (
        PurchaseInvoice.objects.prefetch_related(
            "items__product__uom",
        )
        .select_related(
            "supplier",
        )
        .filter(
            tenant=request.auth,
            supplier=supplier_id,
        )
    )
    filtered_purchases = filters.filter(purchases)
    return filtered_purchases


# suppliers
@supplier_api.get("/all/", response={200: List[SupplierOutSchema]})
@paginate(LimitOffsetPagination)
def supplier_all(request):
    suppliers = Supplier.objects.filter(tenant=request.auth)
    return suppliers


@supplier_api.get("/{supplier_id}/get/", response={200: SupplierOutSchema})
def supplier(request, supplier_id):
    supplier = Supplier.objects.get(tenant=request.auth, id=supplier_id)
    return supplier
