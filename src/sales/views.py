from django.contrib.auth.decorators import login_required
from django.db.models import Sum, ExpressionWrapper, F, DecimalField
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from icecream import ic
from django.db.models.functions import TruncDate
from django.db.models import DateField
from .models import PaymentReceived, SalesInvoice, SalesItem, Customer, Sales
from purchases.utils import number_to_words


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
    payments_received = PaymentReceived.objects.filter(
        tenant=request.tenant,
    ).order_by("-payment_date")

    total_payments_received = payments_received.aggregate(total=Sum("amount"))["total"]
    last_payment = payments_received.first().payment_date

    context = {
        "payments_received": payments_received,
        "total_payments_received": total_payments_received,
        "last_payment": last_payment,
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

    items = [item.quantity for item in sale_items]
    products = [item.product.name for item in sale_items]

    context = {
        "sale_invoice": sale_invoice,
        "sale_items": sale_items,
        "items": items,
        "products": products,
    }
    return render(
        request=request,
        template_name="sales/sales_detail.html",
        context=context,
    )


from datetime import datetime


@login_required
def sales_invoice(request, sales_id):

    sales = get_object_or_404(SalesInvoice, id=sales_id, tenant=request.tenant)
    time = datetime.now()

    sales_items = SalesItem.objects.filter(
        sales=sales.sales,
        tenant=request.tenant,
    ).select_related("product", "sales", "sales__salesinvoice")

    total = sales_items.aggregate(
        total=Sum(
            ExpressionWrapper(
                (F("price") * F("quantity") * F("vat") / 100)
                + (F("price") * F("quantity")),
                output_field=DecimalField(max_digits=20, decimal_places=2),
            ),
        )
    )["total"]

    context = {
        "company": request.tenant,
        "sales": sales,
        "sales_items": sales_items,
        "time": time,
        "total_in_words": number_to_words(total),
    }
    return render(
        request=request, template_name="sales/sales_bill.html", context=context
    )


@login_required
def customer_all(request):
    customers = Customer.objects.filter(tenant=request.tenant)

    context = {
        "customers": customers,
    }
    return render(
        request=request,
        template_name="sales/customer_list.html",
        context=context,
    )


from django.db.models import Sum
from itertools import chain


@login_required
def customer_detail(request, customer_id):
    # Get customer
    customer = Customer.objects.get(id=customer_id)

    # Get all sales invoices for the customer
    invoices = SalesInvoice.objects.filter(
        tenant=request.tenant,
        sales__customer=customer_id,
    ).select_related("sales")

    # Get all payments received from the customer
    payments = PaymentReceived.objects.filter(
        tenant=request.tenant,
        customer=customer_id,
    )

    # Calculate total sales and total payments
    total_sales = (
        invoices.aggregate(total_sales=Sum("total_amount"))["total_sales"] or 0
    )
    total_payments = (
        payments.aggregate(total_payments=Sum("amount"))["total_payments"] or 0
    )

    # Prepare ledger entries
    ledger_entries = []

    # Add invoices to ledger entries
    for invoice in invoices:
        ledger_entries.append(
            {
                "date": invoice.sales.created_at,
                "description": f"Sales Invoice #{invoice.id} (Billing Address: {invoice.billing_address})",
                "debit": invoice.total_amount,
                "credit": None,
                "balance": None,  # To be calculated later
            }
        )

    # Add payments to ledger entries
    for payment in payments:
        ledger_entries.append(
            {
                "date": payment.payment_date,
                "description": f"Payment Received (Payment Method: {payment.payment_method})",
                "debit": None,
                "credit": payment.amount,
                "balance": None,  # To be calculated later
            }
        )

    # Sort all entries by date
    ledger_entries.sort(key=lambda x: x["date"])

    # Calculate running balance
    running_balance = 0
    for entry in ledger_entries:
        if entry["debit"]:
            running_balance += entry["debit"]
        if entry["credit"]:
            running_balance -= entry["credit"]
        entry["balance"] = running_balance

    # Add everything to context
    context = {
        "invoices": invoices,
        "payments": payments,
        "customer": customer,
        "total_sales": total_sales,
        "total_payments": total_payments,
        "ledger_entries": ledger_entries,
        "balance": total_sales - total_payments,
    }

    return render(
        request=request,
        template_name="sales/customer_detail.html",
        context=context,
    )
