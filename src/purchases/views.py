from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy

from fbv.decorators import render_html
import pandas as pd
from decimal import Decimal

from datetime import timedelta
from django.utils import timezone

from purchases.filters import PurchaseFilter, InventoryFilter
from purchases.models import (
    Product,
    PaymentMade,
    PurchaseInvoice,
    PurchaseItem,
    Supplier,
)

from purchases.forms import SupplierEditForm

from sales.models import SalesItem
from core.utils import url


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


@login_required
@render_html("purchase/purchase_index.html")
def purchase_index(request):
    queryset = PurchaseInvoice.objects.filter(
        tenant=request.tenant,
    ).select_related(
        "supplier",
    )
    filter = PurchaseFilter(request.GET, queryset=queryset, tenant=request.tenant)
    context = {"filter": filter}
    return context


@login_required
@render_html("purchase/purchase_add.html")
def purchase_add(request):
    context = {}
    return context


@login_required
@render_html("purchase/purchase_detail.html")
def purchase_detail(request, id):
    purchase = (
        PurchaseInvoice.objects.filter(id=id, tenant=request.tenant)
        .select_related("supplier")
        .first()
    )
    purchase_items = PurchaseItem.objects.filter(
        purchase=purchase,
    ).select_related(
        "purchase",
        "product",
    )

    context = {"purchase": purchase, "purchase_items": purchase_items}
    return context


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
@render_html("supplier/supplier_detail.html")
def supplier_detail(request, supplier_id):
    advance_made_amount = None

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

    if payment_remaining < 0:
        advance_made_amount = abs(payment_remaining)

    context = {
        "advance_made_amount": advance_made_amount,
        "supplier": supplier,
        "supplier_invoice": supplier_invoice,
        "payment_to_be_made": payment_to_be_made,
        "payments_made_amount": payments_made_amount,
        "payment_remaining": payment_remaining,
        "payments_made": payments_made,
    }

    return context


@login_required
def supplier_edit(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)

    if request.method == "POST":
        form = SupplierEditForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request=request, message="Updated Successfully")
            return redirect(reverse_lazy("supplier_list"))
        else:
            messages.error(request=request, message="Some Error Occoured Fix this")

    form = SupplierEditForm(instance=supplier)
    context = {"form": form, "supplier": supplier}
    return render(
        request=request,
        template_name="supplier/supplier_edit.html",
        context=context,
    )


@login_required
@render_html("payments/payments_made.html")
def payments_made(request):
    payments_made = PaymentMade.objects.filter(
        tenant=request.tenant,
    ).select_related(
        "supplier",
    )
    total_payments_made = payments_made.aggregate(total=Sum("amount"))["total"]
    context = {
        "payments_made": payments_made,
        "total_payments_made": total_payments_made,
    }

    return context


@login_required
@render_html("payments/payments_made_create.html")
def payments_made_create(request):
    context = {"suppliers": Supplier.objects.filter(tenant=request.tenant)}
    return context


@login_required
@render_html("inventory/inventory_index.html")
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

    return context


from .models import StockMovement


@login_required
@render_html("inventory/movement.html")
def stock_movement(request):

    movements = StockMovement.objects.filter_by_tenant(request.tenant).select_related(
        "product",
        "tenant",
    )

    context = {
        "movements": movements,
    }
    return context


@login_required
@render_html("purchase/settings.html")
def settings(request):
    return {}


@login_required
@render_html("products/product_details.html")
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

    first_sales = sales.order_by("sales__created_at").first() or None
    last_sales = sales.order_by("-sales__created_at").first() or None

    sales_items = SalesItem.objects.filter(
        tenant=request.tenant, product=product
    ).select_related("sales")

    # Extract relevant data
    sales_qty_list = [item.quantity for item in sales_items]
    sales_time = [
        item.sales.created_at.date().strftime("%Y-%m-%d") for item in sales_items
    ]

    stock_snapshot = [item.stock_snapshot for item in sales_items]

    # Initialize reorder_days
    reorder_days = None
    if first_sales and last_sales:
        days_between_sales = (
            last_sales.sales.created_at - first_sales.sales.created_at
        ).days
        if days_between_sales > 0:
            reorder_days = sold / days_between_sales

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
        "last_sales": last_sales,
    }

    # Only include reorder_days if it was calculated
    if reorder_days is not None:
        context["days_until_reorder"] = reorder_days

    return context


@login_required
def payment_received_list(request): ...


@login_required
@render_html(template_name="purchase/purchase_return.html")
def purchase_return(request, purchase_id: int):
    purchase = PurchaseInvoice.objects.filter(id=purchase_id)

    context = {
        "purchase": purchase,
    }
    return context
