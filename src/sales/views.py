from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render
from icecream import ic

from .models import PaymentReceived, SalesInvoice, SalesItem


@login_required
def sales_add(request):
    context = {}
    return render(
        request=request,
        template_name="sales/sales_add.html",
        context=context,
    )


@login_required
def payments_received(request):
    payments_received = PaymentReceived.objects.filter(tenant=request.tenant)
    total_payments_received = payments_received.aggregate(Sum("amount"))

    context = {
        "payments_received": payments_received,
        "total_payments_received": total_payments_received["amount__sum"],
    }

    return render(
        request=request,
        template_name="payments/payments_received.html",
        context=context,
    )


@login_required
def sales_all(request):
    sales_invoice = (
        SalesInvoice.objects.filter(tenant=request.tenant)
        .select_related("sales__customer")
        .prefetch_related("sales__items__product")
    )

    for invoice in sales_invoice:
        total_vat = sum(item.vat_amount for item in invoice.sales.items.all())
        invoice.total_vat = total_vat
        invoice.with_vat = invoice.total_amount + total_vat

    context = {
        "sales_invoice": sales_invoice,
    }
    return render(
        request=request, template_name="sales/sales_list.html", context=context
    )


@login_required
def sales_detail(request, sales_id):
    sale_invoice = (
        SalesInvoice.objects.filter(tenant=request.tenant, id=sales_id)
        .select_related("sales", "sales__customer")
        .first()
    )

    sale_items = SalesItem.objects.filter(
        sales=sale_invoice.sales, tenant=request.tenant
    ).select_related("product")

    if not sale_invoice:
        raise Http404("SalesInvoice not found")

    ic(sale_items.all)
    ic(sale_invoice)

    context = {
        "sale_invoice": sale_invoice,
        "sale_items": sale_items,
    }
    return render(
        request=request,
        template_name="sales/sales_detail.html",
        context=context,
    )
