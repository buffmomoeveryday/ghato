from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import transaction

from icecream import ic
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django_unicorn.components import UnicornView

from purchases.models import (
    Product,
    PurchaseInovice,
    PurchaseItem,
    Supplier,
    UnitOfMeasurements,
)


class PurchaseAddView(LoginRequiredMixin, UnicornView):

    template_name = "purchase_add_component.html"

    suppliers = []
    uoms = []
    products = []

    new_supplier_name = ""
    new_supplier_address = ""
    new_supplier_contact_person = ""

    supplier = ""
    purchase_invoice_date: date = ""
    purchase_invoice_number = ""
    received_date = date.today()
    total_invoice_amount: float = 0.00

    product = ""
    uom = ""
    quantity = 0
    price = 0.00

    new_product_name = ""
    new_product_uom = ""
    new_product_sku = ""

    received_quantity = 0

    button_disabled = False

    product_to_be_purchased = []

    @transaction.atomic
    def save_all(self):
        if self.purchase_invoice_date is None:
            messages.error(self.request, "Purchase Invoice Date is required")
            raise ValidationError(
                message={"purchase_invoice_date": "The Date is required"},
                code="invalid",
            )
        if self.purchase_invoice_number == "":
            messages.error(self.request, "Supplier Refrence is required")
            raise ValidationError(
                message={"purchase_invoice_number": "Supplier Refrence is required"},
                code="invalid",
            )
        if self.supplier == "":
            messages.error(self.request, "Please Select a supplier")
            raise ValidationError(
                message={"supplier": "Please Select a supplier"},
                code="invalid",
            )

        if not self.product_to_be_purchased:
            messages.error(self.request, "No Items in Invoice")

        try:
            purchase = PurchaseInovice.objects.create(
                supplier_id=self.supplier,
                purchase_date=self.purchase_invoice_date,
                total_amount=self.total_invoice_amount,
                received_date=self.received_date,
                invoice_number=self.purchase_invoice_number,
                tenant=self.request.tenant,
            )
            for item in self.product_to_be_purchased:
                PurchaseItem.objects.create(
                    purchase=purchase,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    price=item["price"],
                    tenant=self.request.tenant,
                )

                product = Product.objects.get(id=item["product_id"])
                product.stock_quantity = item["quantity"]
                product.opening_stock = item["quantity"]
                product.save()

                self.request.session["added_products"] = []

                messages.success(
                    request=self.request,
                    message="Added Successfully",
                )
                return redirect(reverse_lazy("purchase_index"))

        except Exception as e:
            ic(e)
            messages.error(request=self.request, message=f"{e}")

    def remove_item_from_session(self, product_id):
        try:
            self.added_products = self.request.session["added_products"]
            new_added_products = []
            for product in self.added_products:
                if product["product_id"] != str(product_id):
                    new_added_products.append(product)

            self.added_products = new_added_products
            self.product_to_be_purchased = self.added_products
            self.request.session["added_products"] = self.added_products
            messages.success(request=self.request, message="Product Removed")
        except Exception as e:
            messages.error(request=self.request, message=f"Some Error Occurred {e}")

    def add_item_to_session(self):
        try:

            if self.product is None or self.quantity == 0 or self.price == 0:
                return messages.error(request=self.request, message="fix error")

            product_model = Product.objects.get(
                id=self.product,
                tenant=self.request.tenant,
            )

            existing_product = next(
                (
                    p
                    for p in self.product_to_be_purchased
                    if p["product_id"] == self.product
                ),
                None,
            )

            if existing_product:
                if existing_product["price"] != self.price:
                    messages.error(
                        self.request, "Product Already Added With a different rate"
                    )
                    return
                else:
                    existing_product["quantity"] += self.quantity
                    messages.success(
                        self.request, "Product quantity updated successfully."
                    )
            else:
                product = {
                    "product_id": self.product,
                    "product_name": product_model.name,
                    "quantity": (self.quantity),
                    "sku": product_model.sku,
                    "price": float(self.price),
                }
                self.product_to_be_purchased.append(product)
                messages.success(self.request, "Product added successfully.")

            self.request.session["added_products"] = self.product_to_be_purchased

            self.product = ""
            self.price = ""
            self.quantity = ""

        except ValidationError as ve:
            messages.error(self.request, str(ve))

        except Exception as e:
            messages.error(self.request, f"{e}")

    @transaction.atomic
    def create_supplier(self):
        try:
            tenant = self.request.tenant
            supplier = Supplier.objects.create(
                tenant=tenant,
                name=self.new_supplier_name,
                contact_person=self.new_supplier_contact_person,
                address=self.new_supplier_address,
            )
            self.new_supplier_address = ""
            self.new_supplier_contact_person = ""
            self.new_supplier_name = ""

            self.suppliers = Supplier.objects.filter(tenant=self.request.tenant)

            messages.success(
                request=self.request,
                message=f"Supplier {str(supplier.name).capitalize()} Created",
            )
        except Exception as e:
            messages.error(self.request, f"Some error occurred: {e}")

    @transaction.atomic
    def create_product(self):
        try:
            tenant = self.request.tenant
            uom = UnitOfMeasurements.objects.get(id=self.new_product_uom)
            product = Product.objects.create(
                tenant=tenant,
                name=self.new_product_name,
                uom=uom,
                sku=self.new_product_sku,
            )

            self.new_product_sku = ""
            self.new_product_uom = ""
            self.new_product_name = ""

            self.products = Product.objects.filter(tenant=self.request.tenant)

            messages.success(self.request, "Successfully created new product.")

        except Exception as e:
            messages.error(self.request, f"Error: {e}")

    def check_date(self):
        if self.purchase_invoice_date > date.today():
            raise ValidationError(
                {"purchase_invoice_date": "Date cannot be greater than today"},
                code="invalid",
            )

    def edit_product(self, product_id):
        try:
            product = next(
                (
                    p
                    for p in self.product_to_be_purchased
                    if p["product_id"] == str(product_id)
                ),
                None,
            )
            if product:
                self.product = product["product_id"]
                self.quantity = product["quantity"]
                self.price = product["price"]
                messages.success(self.request, "Product details loaded for editing.")
                self.product_to_be_purchased.remove(product)
                self.request.session["added_products"] = self.product_to_be_purchased
            else:
                messages.error(self.request, "Product not found in the session.")
        except Exception as e:
            messages.error(self.request, f"Some Error Occurred: {e}")

    def calculate_total(self):
        self.total_invoice_amount = sum(
            int(item["quantity"]) * float(item["price"])
            for item in self.product_to_be_purchased
        )

    def mount(self):
        self.suppliers = Supplier.objects.filter(tenant=self.request.tenant).order_by(
            "name"
        )
        self.products = Product.objects.filter(tenant=self.request.tenant).order_by(
            "name"
        )
        self.uoms = UnitOfMeasurements.objects.filter(tenant=self.request.tenant)

        if "added_products" not in self.request.session:
            self.request.session["added_products"] = []

        self.product_to_be_purchased = self.request.session["added_products"]

    def complete(self):
        self.calculate_total()

    def updating(self, name, values):
        ic(name)
        ic(values)
