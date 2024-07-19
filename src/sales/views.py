from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import PaymentReceived
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
