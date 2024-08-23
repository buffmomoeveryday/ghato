from django_unicorn.components import UnicornView
from django.db.models import Sum
from typing import List
import json

from purchases.models import PurchaseInvoice, PurchaseItem

from decimal import Decimal
from django.utils.dateformat import DateFormat
from icecream import ic


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


class AnalyticsCharts1View(UnicornView):

    template_name = "analytics_charts_1.html"

    purchase_amounts = []
    top_product_names = []
    top_product_quantites = []
    purchase_dates = []
    suppliers_names = []
    suppliers_amount = []

    def mount(self):

        unformatted_purchase_dates_list = list(
            PurchaseInvoice.objects.filter(tenant=self.request.tenant).values_list(
                "purchase_date", flat=True
            )
        )

        top_products = (
            PurchaseItem.objects.filter(tenant=self.request.tenant)
            .values("product__name")
            .annotate(total_quantity=Sum("quantity"))
            .order_by("-total_quantity")[:5]
        )
        suppliers = (
            PurchaseInvoice.objects.filter(tenant=self.request.tenant)
            .values("supplier__name")
            .annotate(total_amount=Sum("total_amount"))
        )

        self.purchase_amounts = json.dumps(
            list(
                PurchaseInvoice.objects.filter(tenant=self.request.tenant).values_list(
                    "total_amount", flat=True
                )
            ),
            default=decimal_default,
        )
        self.top_product_names = json.dumps(
            list(top_products.values_list("product__name", flat=True)),
            default=decimal_default,
        )
        self.top_product_quantites = json.dumps(
            list(top_products.values_list("total_quantity", flat=True)),
            default=decimal_default,
        )
        self.purchase_dates = json.dumps(
            [
                DateFormat(date).format("Y-m-d")
                for date in unformatted_purchase_dates_list
            ],
            default=decimal_default,
        )
        self.suppliers_names = json.dumps(
            list(suppliers.values_list("supplier__name", flat=True)),
            default=decimal_default,
        )
        self.suppliers_amount = json.dumps(
            list(suppliers.values_list("total_amount", flat=True)),
            default=decimal_default,
        )
