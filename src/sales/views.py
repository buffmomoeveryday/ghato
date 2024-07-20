from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import PaymentReceived, Sales, SalesInvoice, SalesItem
from django.db.models import Sum


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
def sales_list(request):
    sales_invoice = (
        SalesInvoice.objects.filter(tenant=request.tenant)
        .select_related("order__customer")
        .prefetch_related("order__items__product")
    )

    for invoice in sales_invoice:
        total_vat = sum(item.vat_amount for item in invoice.order.items.all())
        invoice.total_vat = total_vat
        invoice.with_vat = invoice.total_amount + total_vat

    context = {
        "sales_invoice": sales_invoice,
    }
    return render(
        request=request, template_name="sales/sales_list.html", context=context
    )
