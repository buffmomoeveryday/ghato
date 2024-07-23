from typing import List

from django.contrib import messages
from django_unicorn.components import UnicornView
from icecream import ic

from sales.models import Customer, Product, Sales, SalesInvoice, SalesItem


class SalesAddComponentView(UnicornView):
    template_name = "sales_add_component.html"

    customers_list = []
    products_list = []
    selected_products = []

    customer: str = ""
    billing_address: str = ""
    product_input: str = ""
    product_price: int = 1
    product_quantity: int = 1
    product_vat: int = 13

    total_amount: float = 0.0
    total_vat: float = 0.0
    product_selected: str = ""

    vat_choices: List[int] = [13, 0]

    def calculate_total(self):
        self.total_amount = sum(item["total"] for item in self.selected_products)

    def calculate_vat(self):
        self.total_vat = sum(
            (item["price"] * item["quantity"] * item["vat"]) / 100
            for item in self.selected_products
        )

    def create_invoice(self):
        try:
            if self.customer == "":
                return messages.error(
                    request=self.request,
                    message="Please Select Customer First",
                )

            customer = Customer.objects.get(id=self.customer)
            sales = Sales.objects.create(
                customer=customer,
                total_amount=self.total_amount,
                tenant=self.request.tenant,
            )

            for item in self.selected_products:
                SalesItem.objects.create(
                    sales=sales,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    price=item["price"],
                    tenant=self.request.tenant,
                )
            SalesInvoice.objects.create(
                order=sales,
                billing_address=self.billing_address,
                total_amount=self.total_amount,
                tenant=self.request.tenant,
            )
            self.selected_products = []
            self.total_amount = 0.0
            self.customer = ""
            self.billing_address = ""
            self.product_selected = ""
            self.total_vat = 0
            messages.success(request=self.request, message="Created Successfully")

        except Exception as e:
            messages.error(request=self.request, message=f"{e}")

    def add_product(self):
        try:
            ic(self.product_selected)

            if (
                self.product_price == 0
                or self.product_quantity == 0
                or self.product_selected is None
            ):
                return messages.error(
                    self.request, "Price or Quantity Could not be zero"
                )
            product = Product.objects.get(id=self.product_selected)

            self.selected_products.append(
                {
                    "product_id": product.id,
                    "product_name": product.name,
                    "quantity": self.product_quantity,
                    "price": self.product_price,
                    "vat": self.product_vat,
                    "vat_amount": (
                        float(self.product_price)
                        * float(self.product_vat)
                        * int(self.product_quantity)
                        / 100
                    ),
                    "total": int(self.product_price) * int(self.product_quantity),
                }
            )
            self.calculate_total()
            self.calculate_vat()
            self.product_input = ""
            self.product_price = 1
            self.product_quantity = 1

        except Product.DoesNotExist:

            self.call("alert", "Product not found")

    def updating(self, name, value):
        ic(name, value)
        return super().updating(name, value)

    def mount(self):
        self.customers_list = Customer.objects.filter(tenant=self.request.tenant)
        self.products_list = Product.objects.filter(
            tenant=self.request.tenant,
            stock_quantity__gt=0,
        )
