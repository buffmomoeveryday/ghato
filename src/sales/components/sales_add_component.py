from typing import List
from django.db import transaction
from django.db.models import Exists, OuterRef
from django.contrib import messages
from django_unicorn.components import UnicornView
from icecream import ic
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from sales.models import Customer, Product, Sales, SalesInvoice, SalesItem
from purchases.models import PurchaseInvoice, PurchaseItem, StockMovement


class SalesAddComponentView(UnicornView):
    template_name = "sales_add_component.html"

    customers_list = []
    products_list = []
    selected_products = []
    original_product_details = []

    customer: str = ""
    billing_address: str = ""

    product_input: str = ""
    product_price: int = 1
    product_quantity: int = 1
    product_vat: int = 13
    product_selected: str = ""
    product_profit: float = 0.00

    total_amount: float = 0.00
    total_vat: float = 0.00
    total_profit: float = 0.00

    vat_choices: List[int] = [13, 0]

    customer_first_name: str = ""
    customer_last_name: str = ""
    customer_phone: int = 0  # Default to 0 instead of an empty string
    customer_address: str = ""
    customer_email: str = ""

    product_cost: float = 0.00
    product_stock = 0

    disable_add_product_btn = False
    disable_edit_btn = False

    # TODO: Implement a feature where I can directly change the invoice's payment status
    is_paid = False

    def calculate_total(self):
        self.total_amount = sum(item["total"] for item in self.selected_products)

    def calculate_vat(self):
        self.total_vat = sum(
            (item["price"] * item["quantity"] * item["vat"]) / 100
            for item in self.selected_products
        )

    def calculate_profit(self):
        self.total_profit = sum(
            float(item["product_profit"]) for item in self.selected_products
        )

    @transaction.atomic
    def create_invoice(self):
        try:
            if not self.customer:
                return messages.error(
                    request=self.request, message="Please Select Customer First"
                )
            customer = Customer.objects.get(
                id=self.customer, tenant=self.request.tenant
            )
            sales = Sales.objects.create(
                customer=customer,
                total_amount=self.total_amount,
                tenant=self.request.tenant,
            )

            for item in self.selected_products:
                product = Product.objects.get(
                    id=item["product_id"], tenant=self.request.tenant
                )
                salesitem = SalesItem.objects.create(
                    sales=sales,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    price=item["price"],
                    tenant=self.request.tenant,
                    vat=item["vat"],
                    stock_snapshot=product.stock_quantity,
                )
                salesitem.save()
                product.stock_quantity -= item["quantity"]
                product.save()
                StockMovement.objects.create(
                    product=product,
                    quantity=item["quantity"],
                    movement_type="OUT",
                    description=f"Sold to {customer.get_full_name}",
                    tenant=self.request.tenant,
                )

            SalesInvoice.objects.create(
                sales=sales,
                billing_address=self.billing_address,
                total_amount=self.total_amount,
                created_by=self.request.user,
                tenant=self.request.tenant,
            )
            self.selected_products = []
            self.total_amount = 0.0
            self.customer = ""
            self.billing_address = ""
            self.product_selected = ""
            self.total_vat = 0
            self.product_price = 0
            self.total_profit = 0.00
            self.product_quantity = 0
            messages.success(request=self.request, message="Created Successfully")

        except Exception as e:
            messages.error(request=self.request, message=f"{e}")
            raise e

    @transaction.atomic
    def create_customer(self):
        try:
            first_name = self.customer_first_name
            last_name = self.customer_last_name
            number = self.customer_phone
            address = self.customer_address
            email = self.customer_email

            customer = Customer.objects.create(
                first_name=first_name,
                last_name=last_name,
                phone_number=number,
                address=address,
                email=email,
                tenant=self.request.tenant,
            )
            self.customers_list = Customer.objects.filter(tenant=self.request.tenant)
            messages.success(self.request, "Customer Created")

        except Exception as e:
            ic(e)

    def add_product(self):
        try:
            if not self.product_selected.strip():
                raise ValidationError(
                    {"product_selected": "Select a product"}, code="required"
                )

            if (
                self.product_price <= 0
                or self.product_quantity <= 0
                or not self.product_selected.strip()
            ):
                return messages.error(
                    self.request, "Price or Quantity or Product Could not be zero"
                )
            for item in self.selected_products:
                if item["product_id"] == int(self.product_selected):
                    messages.error(self.request, "Product already added")
                    raise ValidationError(
                        {"product_selected": "Already Added Product"},
                        code="invalid",
                    )

            self.validate_quantity()
            product = (
                Product.objects.filter(id=self.product_selected)
                .prefetch_related("purchase_item")
                .first()
            )
            purchase_item = PurchaseItem.objects.get(
                product=product, tenant=self.request.tenant
            )
            ic(self.product_quantity, self.product_price, purchase_item.price)
            self.product_profit = self.product_quantity * (
                self.product_price - purchase_item.price
            )
            self.selected_products.append(
                {
                    "product_id": product.id,
                    "product_name": product.name,
                    "quantity": self.product_quantity,
                    "price": self.product_price,
                    "vat": self.product_vat,
                    "product_profit": self.product_profit,
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
            self.calculate_profit()
            self.product_input = ""
            self.product_price = 1
            self.product_quantity = 1

        except Product.DoesNotExist:
            self.call("alert", "Product not found")

        except Exception as e:
            ic(e)
            raise e

    def validate_quantity(self):
        if not self.product_selected.strip():
            messages.error(self.request, "Select A Product First")
            raise ValidationError(
                {"product_selected": "Select A Product"},
                code="invalid",
            )
        product = Product.objects.get(
            id=self.product_selected, tenant=self.request.tenant
        )

        if product.stock_quantity < self.product_quantity:
            messages.error(self.request, "Please Fix")
            raise ValidationError(
                {
                    "product_quantity": f"The quantity cannot be greater than {product.stock_quantity}"
                },
                code="invalid",
            )

    def remove_item(self, item_id: int):
        try:
            item = next(
                item for item in self.selected_products if item["product_id"] == item_id
            )
            if item:
                self.selected_products.remove(item)

                self.calculate_vat()
                self.calculate_total()

                messages.success(self.request, "Item Removed")

                self.product_input = ""
                self.product_price = 1
                self.product_quantity = 1
                self.product_vat = 13
                self.product_selected = ""

            else:
                messages.error(self.request, "Not Found")

        except Exception as e:
            messages.error(self.request, f"Some error {e}")

    def edit_item(self, item_id):
        if not self.disable_edit_btn:
            try:
                self.disable_edit_btn = True

                item = next(
                    item
                    for item in self.selected_products
                    if item["product_id"] == item_id
                )
                if item:
                    self.original_product_details = item.copy()
                    self.product_input = item["product_name"]
                    self.product_price = item["price"]
                    self.product_quantity = item["quantity"]
                    self.product_vat = item["vat"]
                    self.product_profit = item["product_profit"]
                    self.product_selected = str(item["product_id"])

                    self.selected_products.remove(item)

                    messages.success(self.request, "Loaded For Editing")

            except Exception as e:
                self.disable_edit_btn = False
                ic(e)

    def cancel_editing(self):
        if self.original_product_details:
            self.selected_products.append(self.original_product_details)

            self.disable_edit_btn = False
            self.product_input = ""
            self.product_price = 1
            self.product_quantity = 1
            self.product_vat = 13
            self.product_selected = ""
            self.original_product_details = []

    def mount(self):
        self.customers_list = Customer.objects.filter(tenant=self.request.tenant)
        self.products_list = (
            Product.objects.filter(
                tenant=self.request.tenant,
                stock_quantity__gt=0,
            )
            .annotate(
                has_purchase=Exists(PurchaseItem.objects.filter(product=OuterRef("pk")))
            )
            .filter(has_purchase=True)
            .order_by("name")
        )

    def get_details(self):
        self.product_cost = (
            PurchaseItem.objects.filter(product__id=self.product_selected).first().price
        )
        self.product_stock = (
            Product.objects.filter(id=self.product_selected).first().stock_quantity
        )

    def print_hello(self):
        print(":hell")

    def updating(self, name, value):
        ic(name, value)
