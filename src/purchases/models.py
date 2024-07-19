from django.db import models

from core.models import BaseModelMixin
from tenant.models import TenantAwareModel


class UnitOfMeasurements(TenantAwareModel, BaseModelMixin):

    class FieldType(models.TextChoices):
        CURRENT = "1", ""
        SAVING = "2", "SAVING"

    name = models.CharField(max_length=100)
    field = models.CharField(
        choices=FieldType.choices,
        default=FieldType.CURRENT,
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Product(TenantAwareModel, BaseModelMixin):
    # TODO: add product category

    name = models.CharField(max_length=100)
    uom = models.ForeignKey(UnitOfMeasurements, on_delete=models.SET_NULL, null=True)
    sku = models.CharField(max_length=50, unique=True)
    stock_quantity = models.IntegerField(null=True)
    # vat_percentage = models.CharField(verbose_name="Vat Percentage",``)

    def __str__(self):
        return self.name


class StockMovement(TenantAwareModel, BaseModelMixin):
    MOVEMENT_TYPE_CHOICES = [
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.movement_type} ({self.quantity})"


class PaymentMade(TenantAwareModel, BaseModelMixin):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey("Supplier", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.amount} paid"


class Supplier(TenantAwareModel, BaseModelMixin):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class PurchaseInovice(TenantAwareModel, BaseModelMixin):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    invoice_number = models.CharField(
        verbose_name="Purchase Invoice Number",
        null=True,
        blank=True,
        max_length=10,
    )
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    received_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Purchase #{self.id} - {self.supplier.name}"


class PurchaseItem(TenantAwareModel, BaseModelMixin):
    purchase = models.ForeignKey(
        PurchaseInovice,
        related_name="items",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total(self):
        return self.price * self.quantity
