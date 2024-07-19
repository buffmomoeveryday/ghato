from sales.models import Customer, Product, Sales, SalesItem, SalesInvoice
from icecream import ic

from django.contrib import messages
from django_unicorn.components import UnicornView


class SalesAddComponentView(UnicornView):
    template_name = "sales_add_component.html"

    customers_list = []
    products_list = []
    selected_products = []

    customer = ""
    billing_address = ""
    product_input = ""
    product_price: int = 1
    product_quantity: int = 1
    total_amount = 0.0

    product_selected = ""

    def mount(self):
        self.customers_list = Customer.objects.filter(tenant=self.request.tenant)
        self.products_list = Product.objects.filter(
            tenant=self.request.tenant,
            stock_quantity__gt=0,
        )

    def updating(self, name, value):
        ic(name, value)
        return super().updating(name, value)

    def calculate_total(self):
        self.total_amount = sum(item["total"] for item in self.selected_products)

    def create_invoice(self):
        try:
            if self.customer == "":
                return messages.error(
                    request=self.request,
                    message="Please Select Customer First",
                )

            customer = Customer.objects.get(id=self.customer)
            sales_order = Sales.objects.create(
                customer=customer,
                total_amount=self.total_amount,
                tenant=self.request.tenant,
            )

            for item in self.selected_products:
                SalesItem.objects.create(
                    order=sales_order,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    price=item["price"],
                    tenant=self.request.tenant,
                )
            SalesInvoice.objects.create(
                order=sales_order,
                billing_address=self.billing_address,
                total_amount=self.total_amount,
                tenant=self.request.tenant,
            )
            self.selected_products = []
            self.total_amount = 0.0
            self.customer = ""
            self.billing_address = ""
            self.product_selected = ""

        except Exception as e:
            ic(e)
            messages.error(request=self.request, message=f"{e}")

    def add_product(self):
        try:
            product = Product.objects.get(id=self.product_selected)
            ic(product)
            ic(product.id)
            self.selected_products.append(
                {
                    "product_id": product.id,
                    "product_name": product.name,
                    "quantity": self.product_quantity,
                    "price": self.product_price,
                    "total": int(self.product_price) * int(self.product_quantity),
                }
            )
            self.calculate_total()
            self.product_input = ""
            self.product_price = 1
            self.product_quantity = 1

        except Product.DoesNotExist:
            self.call("alert", "Product not found")
