from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django_unicorn.components import UnicornView
from django_unicorn.components import LocationUpdate, UnicornView, HashUpdate
from icecream import ic
from django.shortcuts import redirect
from django.urls import reverse_lazy

from purchases.models import (
    Product,
    Supplier,
    UnitOfMeasurements,
    PurchaseInovice,
    PurchaseItem,
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
    received_date = ""
    total_invoice_amount = 0

    product = ""
    uom = ""
    quantity = 0
    price = 0

    new_product_name = ""
    new_product_uom = ""
    new_proudct_sku = ""

    received_quantity = 0

    button_disabled = False

    product_to_be_purchased = []

    @transaction.atomic
    def save_all(self):
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
                self.request.session["added_products"] = []
                messages.success(
                    request=self.request,
                    message="Added Successfully",
                )
                return redirect(reverse_lazy("purchase_index"))

        except Exception as e:
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
            messages.success(request=self.request, message="Proudct Removed")

        except Exception as e:
            messages.error(request=self.request, message=f"Some Error Occoured {e}")

    def add_item_to_session(self):
        try:
            product_model = Product.objects.get(
                id=self.product,
                tenant=self.request.tenant,
            )

            product = {
                "product_id": self.product,
                "product_name": product_model.name,
                "quantity": self.quantity,
                "sku": product_model.sku,
                "price": self.price,
            }

            self.product_to_be_purchased.append(product)
            self.request.session["added_products"] = self.product_to_be_purchased
            ic(self.request.session["added_products"])

            self.product = ""
            self.price = ""
            self.quantity = ""
            messages.success(request=self.request, message="Product Added Successfully")

        except Exception as e:
            messages.error(request=self.request, message=f"{e}")

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
                message=f"Supplier {str(supplier.name).capitalize} Created",
            )
        except Exception as e:
            messages.error(request=self.request, message=f"Some error occoured {e}")

    @transaction.atomic
    def create_product(self):
        try:
            tenant = self.request.tenant
            uom = UnitOfMeasurements.objects.get(id=self.new_product_uom)
            ic(uom)
            product = Product.objects.create(
                tenant=tenant,
                name=self.new_product_name,
                uom=uom,
                sku=self.new_proudct_sku,
            )

            self.new_proudct_sku = ""
            self.new_product_uom = ""
            self.new_product_name = ""

            messages.success(
                request=self.request,
                message=f"Sucessfully Created new Product",
            )

        except Exception as e:
            messages.error(request=self.request, message=f"Error{e}")

    def check_date(self):
        if self.purchase_invoice_date >= date.today():
            raise ValidationError(
                {"purchase_invoice_date": "Date Cannot Be Greater than today"},
                code="invalid",
            )

    def mount(self):
        self.suppliers = Supplier.objects.filter(
            tenant=self.request.tenant,
        )
        self.products = Product.objects.filter(
            tenant=self.request.tenant,
        )
        self.uoms = UnitOfMeasurements.objects.filter(
            tenant=self.request.tenant,
        )

        if "added_products" not in self.request.session:
            self.request.session["added_products"] = []

        self.product_to_be_purchased = self.request.session["added_products"]
