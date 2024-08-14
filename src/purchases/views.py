from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.http import HttpResponse
from django.db import transaction
from .filters import PurchaseFilter
from .models import PaymentMade, PurchaseInvoice, PurchaseItem, Supplier
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
        model = PurchaseInvoice
        fields = ["supplier", "total_amount", "received_date"]


class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ["product", "quantity", "price"]


@login_required
def purchase_index(request):
    queryset = PurchaseInvoice.objects.filter(tenant=request.tenant).select_related(
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
            PurchaseInvoice.objects.filter(id=id, tenant=request.tenant)
            .select_related("supplier")
            .first()
        )
        purchase_items = PurchaseItem.objects.filter(purchase=purchase).select_related(
            "purchase", "product"
        )

        context = {
            "purchase": purchase,
            "purchase_items": purchase_items,
            # "purchase_dates": json.dumps(formatted_dates, default=decimal_default),
            # "purchase_amounts": json.dumps(
            #     list(purchase_amounts), default=decimal_default
            # ),
            # "top_products_names": json.dumps(
            #     list(top_products.values_list("product__name", flat=True)),
            #     default=decimal_default,
            # ),
            # "top_products_quantities": json.dumps(
            #     list(top_products.values_list("total_quantity", flat=True)),
            #     default=decimal_default,
            # ),
            # "suppliers_names": json.dumps(
            #     list(suppliers.values_list("supplier__name", flat=True)),
            #     default=decimal_default,
            # ),
            # "suppliers_amounts": json.dumps(
            #     list(suppliers.values_list("total_amount", flat=True)),
            #     default=decimal_default,
            # ),
        }
        return render(
            request=request,
            template_name="purchase/purchase_detail.html",
            context=context,
        )


@login_required
def supplier_list(request):
    suppliers = Supplier.objects.filter(tenant=request.tenant)
    context = {"suppliers": suppliers}
    return render(
        request=request,
        template_name="supplier/supplier_list.html",
        context=context,
    )


@login_required
def supplier_detail(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id, tenant=request.tenant)
    supplier_invoice = PurchaseInvoice.objects.filter(
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


@login_required
def payments_made_create(request):

    # if request.method == "POST":

    #     amount = request.POST.get("amount")
    #     payment_method = request.POST.get("payment_method")
    #     payment_date = request.POST.get("payment_date")
    #     transaction_id = request.POST.get("transaction_id")
    #     supplier_id = request.POST.get("supplier_id")

    #     bank = request.POST.get("bank_id")
    #     cash = request.POST.get("cash_id")

    #     with transaction.atomic():
    #         payment_made = PaymentMade.objects.create(
    #             amount=amount,
    #             payment_method=payment_method,
    #             payment_date=payment_date,
    #             transaction_id=transaction_id,
    #             supplier=supplier_id,
    #         )

    context = {"suppliers": Supplier.objects.filter(tenant=request.tenant)}

    return render(
        request=request,
        template_name="payments/payments_made_create.html",
        context=context,
    )


import datetime
from .filters import InventoryFilter


@login_required
def inventory(request):

    tenant = request.user.tenant
    purchase_items = PurchaseItem.objects.filter(
        tenant=tenant,
        product__stock_quantity__gte=1,
    ).select_related(
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


from datetime import timedelta
from django.utils import timezone


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

    first_sales = sales.order_by("sales__created_at").first()
    last_sales = sales.order_by("-sales__created_at").first()

    sales_items = SalesItem.objects.filter(
        tenant=request.tenant, product=product
    ).select_related("sales")

    # Extract relevant data
    sales_qty_list = [item.quantity for item in sales_items]
    sales_time = [
        item.sales.created_at.date().strftime("%Y-%m-%d") for item in sales_items
    ]
    for items in sales_items:
        ic(items.stock_snapshot)

    stock_snapshot = [item.stock_snapshot for item in sales_items]

    # Initialize reorder_days
    reorder_days = None
    if first_sales and last_sales:
        days_between_sales = (
            last_sales.sales.created_at - first_sales.sales.created_at
        ).days
        if days_between_sales > 0:
            reorder_days = sold / days_between_sales

    ic(reorder_days)
    remaining_stock = opening_stock - sold

    try:
        sell_through_rate = (sold / opening_stock) * 100
    except ZeroDivisionError:
        sell_through_rate = 0

    # Calculate sales trend
    today = timezone.now().date()
    start_date = today - timedelta(days=30)
    period1_start = start_date + timedelta(days=15)

    # First period (last 15 days)
    period1_sales = sales_items.filter(sales__created_at__date__gte=period1_start)
    period1_total = sum(item.quantity for item in period1_sales)

    # Second period (previous 15 days)
    period2_sales = sales_items.filter(
        sales__created_at__date__lt=period1_start,
        sales__created_at__date__gte=start_date,
    )
    period2_total = sum(item.quantity for item in period2_sales)

    if period2_total > 0:
        sales_trend = ((period1_total - period2_total) / period2_total) * 100
    else:
        sales_trend = 0  # If no sales in the previous period, set trend to 0

    # Round sales trend for better readability
    sales_trend = round(sales_trend, 2)

    context = {
        "product": product,
        "sales": sales,
        "sell_through_rate": round(sell_through_rate, 3),
        "opening_stock": opening_stock,
        "remaining_stock": remaining_stock,
        "sales_qty_list": sales_qty_list,
        "sales_time": sales_time,
        "stock_snapshot": stock_snap_shot,
        "product": product,
        "sell_through_rate": round(sell_through_rate, 3),
        "opening_stock": opening_stock,
        "remaining_stock": remaining_stock,
        "sales_qty_list": sales_qty_list,
        "sales_time": sales_time,
        "sales_trend": sales_trend,  # Pass the calculated sales trend
        "stock_snapshot": stock_snapshot,  # Pass stock snapshot data
    }

    # Only include reorder_days if it was calculated
    if reorder_days is not None:
        context["days_until_reorder"] = reorder_days

    return render(
        request=request,
        template_name="products/product_details.html",
        context=context,
    )
