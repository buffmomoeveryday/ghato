from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, Count, Avg, ExpressionWrapper
from django.db.models import DecimalField

from datetime import datetime, timedelta

from purchases.models import *
from sales.models import *

from icecream import ic


from django.shortcuts import render
from django.db.models import Sum, Count, Avg
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import json


@login_required()
def dashboard_index(request):
    start_date = datetime.now() - timedelta(days=30)

    total_sales = Sales.objects.filter(
        created_at__gte=start_date,
        tenant=request.tenant,
    ).aggregate(Sum("total_amount"))["total_amount__sum"]

    total_sales_made = (
        Sales.objects.filter(tenant=request.tenant).aggregate(
            total_amount=Sum("total_amount")
        )["total_amount"]
        or 0
    )

    total_purchases_made = (
        PurchaseInvoice.objects.filter(tenant=request.tenant).aggregate(
            total_amount=Sum("total_amount")
        )["total_amount"]
        or 0
    )

    total_stock_remaining = (
        PurchaseItem.objects.filter(tenant=request.tenant)
        .annotate(
            total_value=ExpressionWrapper(
                F("quantity") * F("price"), output_field=DecimalField()
            )
        )
        .aggregate(total_value_sum=Sum("total_value"))["total_value_sum"]
        or 0
    )
    total_payments_made = (
        PaymentMade.objects.filter(tenant=request.tenant).aggregate(
            total_value=Sum("amount")
        )["total_value"]
        or 0
    )

    cogs = total_purchases_made - total_stock_remaining
    profit = total_sales_made - cogs

    top_selling_products = list(
        SalesItem.objects.filter(tenant=request.tenant)
        .values("product__name")
        .annotate(
            total_sold=Sum("quantity"),
        )
        .order_by("-total_sold")[:5]
    )

    customer_purchases = list(
        Sales.objects.filter(tenant=request.tenant)
        .values(
            "customer__first_name",
            "customer__last_name",
        )
        .annotate(purchase_count=Count("id"))
        .order_by("-purchase_count")[:5]
    )

    customer_avg_order_value = Sales.objects.filter(
        tenant=request.tenant,
    ).aggregate(avg_order_value=Avg("total_amount"))

    total_payments_received = PaymentReceived.objects.filter(
        payment_date__gte=start_date,
        tenant=request.tenant,
    ).aggregate(Sum("amount"))["amount__sum"]

    unpaid_invoices = SalesInvoice.objects.filter(
        payment_status="Unpaid",
        tenant=request.tenant,
    ).select_related("sales__customer")[:5]

    context = {
        "total_sales": total_sales or 0,
        "top_selling_products_data": json.dumps(
            [
                {"x": item["product__name"], "y": item["total_sold"]}
                for item in top_selling_products
            ]
        ),
        "customer_purchases_data": json.dumps(
            [
                {
                    "x": f"{item['customer__first_name']} {item['customer__last_name']}",
                    "y": item["purchase_count"],
                }
                for item in customer_purchases
            ]
        ),
        "customer_avg_order_value": customer_avg_order_value["avg_order_value"] or 0,
        "total_payments_received": total_payments_received or 0,
        "unpaid_invoices": [
            {
                "id": invoice.id,
                "customer_name": invoice.sales.customer.get_full_name,
                "total_amount": float(invoice.total_amount),
                "payment_status": invoice.payment_status,
            }
            for invoice in unpaid_invoices
        ],
        "profit": profit,
        "cogs": cogs,
        "total_stock_remaining": total_stock_remaining,
        "total_purchase_made": total_purchases_made,
        "total_sales_made": total_sales_made,
        "total_payments_made": total_payments_made,
    }

    return render(request, "dashboard/dashboard-index.html", context)


@login_required()
def add_uom(request):
    if request.method == "POST":
        uom = request.POST.get("UOM")
        unit_of_measurements = UnitOfMeasurements.objects.get_or_create(name="uom")


from django.http import JsonResponse
from .sqlutils import process_natural_language_query


from django.http import StreamingHttpResponse
import time


@login_required
def chat(request):
    if request.method == "GET":
        return render(request=request, template_name="dashboard/query.html")
    if request.method == "POST":
        nl_query = request.POST.get("query", "")
        result = process_natural_language_query(nl_query, request.tenant.id)
        return JsonResponse(result)

    return JsonResponse({"error": "Only GET and POST requests are allowed"}, status=405)
