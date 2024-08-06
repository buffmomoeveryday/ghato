from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .filters import PurchaseFilter
from .models import PaymentMade, PurchaseInovice, PurchaseItem, Supplier
from sales.models import SalesItem

import pandas as pd
import json
from django.utils.dateformat import DateFormat
from decimal import Decimal


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = PurchaseInovice
        fields = ["supplier", "total_amount", "received_date"]


class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ["product", "quantity", "price"]


@login_required
def purchase_index(request):
    queryset = PurchaseInovice.objects.filter(tenant=request.tenant).select_related(
        "supplier"
    )
    filter = PurchaseFilter(request.GET, queryset=queryset, tenant=request.tenant)
    context = {
        "filter": filter,
    }
    return render(request, "purchase/purchase_index.html", context)


@login_required
def purchase_add(request):
    context = {}
    return render(
        request=request,
        template_name="purchase/purchase_add.html",
        context=context,
    )


@login_required
def purchase_detail(request, id):
    if request.method == "GET":
        purchase = (
            PurchaseInovice.objects.filter(id=id, tenant=request.tenant)
            .select_related("supplier")
            .first()
        )
        purchase_items = PurchaseItem.objects.filter(purchase=purchase).select_related(
            "purchase", "product"
        )

        # Data for charts
        purchase_dates = list(
            PurchaseInovice.objects.values_list("purchase_date", flat=True)
        )
        formatted_dates = [DateFormat(date).format("Y-m-d") for date in purchase_dates]
        purchase_amounts = list(
            PurchaseInovice.objects.values_list("total_amount", flat=True)
        )
        top_products = (
            PurchaseItem.objects.values("product__name")
            .annotate(total_quantity=Sum("quantity"))
            .order_by("-total_quantity")[:5]
        )
        suppliers = PurchaseInovice.objects.values("supplier__name").annotate(
            total_amount=Sum("total_amount")
        )

        context = {
            "purchase": purchase,
            "purchase_items": purchase_items,
            "purchase_dates": json.dumps(formatted_dates, default=decimal_default),
            "purchase_amounts": json.dumps(
                list(purchase_amounts), default=decimal_default
            ),
            "top_products_names": json.dumps(
                list(top_products.values_list("product__name", flat=True)),
                default=decimal_default,
            ),
            "top_products_quantities": json.dumps(
                list(top_products.values_list("total_quantity", flat=True)),
                default=decimal_default,
            ),
            "suppliers_names": json.dumps(
                list(suppliers.values_list("supplier__name", flat=True)),
                default=decimal_default,
            ),
            "suppliers_amounts": json.dumps(
                list(suppliers.values_list("total_amount", flat=True)),
                default=decimal_default,
            ),
        }
        return render(
            request=request,
            template_name="purchase/purchase_detail.html",
            context=context,
        )


@login_required
def supplier_detail(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id, tenant=request.tenant)
    supplier_invoice = PurchaseInovice.objects.filter(
        supplier=supplier, tenant=request.tenant
    )
    payments_made = PaymentMade.objects.filter(supplier=supplier, tenant=request.tenant)
    payment_to_be_made = (
        supplier_invoice.aggregate(Sum("total_amount"))["total_amount__sum"] or 0
    )

    payments_made_amount = payments_made.aggregate(Sum("amount"))["amount__sum"] or 0
    payment_remaining = payment_to_be_made - payments_made_amount

    context = {
        "supplier": supplier,
        "supplier_invoice": supplier_invoice,
        "payment_to_be_made": payment_to_be_made,
        "payments_made_amount": payments_made_amount,
        "payment_remaining": payment_remaining,
        "payments_made": payments_made,
    }
    return render(request, "supplier/supplier_detail.html", context)


@login_required
def payments_made(request):
    payments_made = PaymentMade.objects.filter(tenant=request.tenant).select_related(
        "supplier"
    )
    total_payments_made = payments_made.aggregate(Sum("amount"))
    context = {
        "payments_made": payments_made,
        "total_payments_made": total_payments_made["amount__sum"],
    }

    return render(
        request=request, template_name="payments/payments_made.html", context=context
    )


import datetime
from .filters import InventoryFilter


@login_required
def inventory(request):

    tenant = request.user.tenant
    purchase_items = PurchaseItem.objects.filter(tenant=tenant).select_related(
        "product",
        "tenant",
        "purchase__supplier",
        "product__uom",
    )

    filter = InventoryFilter(
        request.GET, queryset=purchase_items, tenant=request.tenant
    )

    total_inventory_value = (
        purchase_items.annotate(
            total_value=ExpressionWrapper(
                F("quantity") * F("price"), output_field=DecimalField()
            )
        ).aggregate(total_value_sum=Sum("total_value"))["total_value_sum"]
        or 0
    )

    context = {
        "inventory": filter.qs,
        "inventory_form": filter.form,
        "total_inventory_value": total_inventory_value,
    }

    return render(
        request=request,
        template_name="inventory/inventory_index.html",
        context=context,
    )


from .models import Product
from icecream import ic


@login_required
def stock_movement(request):
    sales = SalesItem.objects.filter_by_tenant(request.tenant).select_related(
        "product",
        "sales",
        "sales__customer",
    )

    context = {
        "sales": sales,
    }
    return render(
        request=request,
        template_name="inventory/movement.html",
        context=context,
    )


@login_required
def settings(request):
    context = {}
    return render(
        request=request,
        template_name="purchase/settings.html",
        context=context,
    )


@login_required
def product_analytics(request, product_id):

    product = get_object_or_404(Product, id=product_id, tenant=request.tenant)

    purchase = PurchaseItem.objects.filter(
        tenant=request.tenant, product=product
    ).select_related()
    sales = SalesItem.objects.filter(
        tenant=request.tenant,
        product=product,
    ).select_related(
        "product",
        "sales",
        "sales__customer",
    )

    opening_stock = product.opening_stock or 0

    sales_qty_list = list(item.quantity for item in sales)
    sales_time = list(str((item.created_at).date()) for item in sales)

    stock_snap_shot = list(item.stock_snapshot for item in sales)
    sold = sum(sales_qty_list)

    remaining_stock = opening_stock - sold

    try:
        sell_through_rate = (sold / opening_stock) * 100

    except ZeroDivisionError as _:
        sell_through_rate = 0

    context = {
        "product": product,
        "sales": sales,
        "sell_through_rate": round(sell_through_rate, 3),
        "opening_stock": opening_stock,
        "remaining_stock": remaining_stock,
        "sales_qty_list": sales_qty_list,
        "sales_time": sales_time,
        "stock_snapshot": stock_snap_shot,
    }
    return render(
        request=request,
        template_name="products/product_details.html",
        context=context,
    )
