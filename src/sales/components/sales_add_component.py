from typing import List
from django.db import transaction
from django.db.models import Exists, OuterRef
from django.contrib import messages
from django_unicorn.components import UnicornView
from icecream import ic
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from sales.models import Customer, Product, Sales, SalesInvoice, SalesItem
from purchases.models import PurchaseInovice, PurchaseItem


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

    total_amount: float = 0.00
    total_vat: float = 0.00

    vat_choices: List[int] = [13, 0]

    disable_add_product_btn = False
    disable_edit_btn = False

    def calculate_total(self):
        self.total_amount: float = sum(item["total"] for item in self.selected_products)

    def calculate_vat(self):
        self.total_vat = sum(
            (item["price"] * item["quantity"] * item["vat"]) / 100
            for item in self.selected_products
        )

    @transaction.atomic
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
                salesitem = SalesItem.objects.create(
                    sales=sales,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    price=item["price"],
                    tenant=self.request.tenant,
                    vat=item["vat"],
                )

                product = Product.objects.get(id=item["product_id"])

                salesitem.stock_snapshop = product.stock_quantity
                salesitem.save()

                product.stock_quantity = product.stock_quantity - item["quantity"]
                product.save()

            SalesInvoice.objects.create(
                sales=sales,
                billing_address=self.billing_address,
                total_amount=self.total_amount,
                tenant=self.request.tenant,
                created_by=self.request.user,
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
            raise e

    def add_product(self):
        try:
            if (
                self.product_price == 0
                or self.product_quantity == 0
                or self.product_selected == " "
            ):
                return messages.error(
                    self.request, "Price or Quantity Could not be zero"
                )
            for item in self.selected_products:
                if item["product_id"] == int(self.product_selected):
                    messages.error(self.request, "Product already added")
                    raise ValidationError(
                        {"product_selected": f"Already Added Product"},
                        code="invalid",
                    )

            self.validate_quantity()
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

    def validate_quantity(self):

        if self.product_selected == None or self.product_selected == " ":
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
        else:
            pass

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

                self.product_input: str = ""
                self.product_price: int = 1
                self.product_quantity: int = 1
                self.product_vat: int = 13
                self.product_selected: str = ""

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
