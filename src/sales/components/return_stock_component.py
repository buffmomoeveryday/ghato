from django_tasks.task import ResultStatus
from django.urls import reverse_lazy
from django.db import transaction
from django.utils.timezone import now
from django.shortcuts import redirect
from django.contrib import messages
from icecream import ic

from django_unicorn.components import UnicornView

from sales.tasks import fix_returned_stocks
from sales.models import Sales, SalesInvoice, SalesItem, Product
from purchases.models import PurchaseItem, Product, StockMovement


class ReturnStockComponentView(UnicornView):
    template_name = "return_stock_component.html"
    sales_id: int = None

    def mount(self):
        self.sales_id = self.component_kwargs["sales_id"]

    def trigger_return(self, sales_id):
        try:
            sales_invoice = SalesInvoice.objects.filter(
                id=sales_id, tenant=self.request.tenant
            ).first()
            sale_items = sales_invoice.sales.items.filter(tenant=self.request.tenant)
            with transaction.atomic():
                for item in sale_items:
                    product = Product.objects.get(id=item.product.id)
                    product.stock_quantity += item.quantity
                    product.save()
                    StockMovement.objects.create(
                        product=product,
                        quantity=item.quantity,
                        movement_type="IN SALES RETURN",
                        description=f"Sales returned invoice number {sales_id}",
                        created_by=self.request.user,
                    )

                sales_invoice.sales.delete()

            messages.success(self.request, "Deleted Successfully")
            return redirect(reverse_lazy("sales_list"))

        except Exception as e:
            self.call("refresh_page()")
            return messages.error(
                self.request, "Some Error occoured cannot return teh stock "
            )
