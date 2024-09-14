from datetime import timedelta
from typing import Optional

from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import BaseModelMixin
from tenant.models import TenantAwareModel
from .managers import ReturnManagers

from icecream import ic


class UnitOfMeasurements(TenantAwareModel, BaseModelMixin):

    class FieldType(models.TextChoices):
        FLOAT = "FLOAT", "Float"
        INT = "INTEGER", "Integer"

    name = models.CharField(max_length=100)

    field = models.CharField(
        choices=FieldType.choices,
        default=FieldType.FLOAT,
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Product(TenantAwareModel, BaseModelMixin):
    name = models.CharField(max_length=100)
    uom = models.ForeignKey(UnitOfMeasurements, on_delete=models.SET_NULL, null=True)
    sku = models.CharField(max_length=50, unique=True)
    stock_quantity = models.FloatField(null=True)
    opening_stock = models.IntegerField(null=True)

    def __str__(self):
        return self.name


#####################
### STOCK MOVEMENT###
###################``#


class StockMovement(TenantAwareModel, BaseModelMixin):
    MOVEMENT_TYPE_CHOICES = [
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
        ("IN SALES RETURN", "Stock In Sales Return"),
        ("OUT PURCHASE RETURN", "Stock Out Purchase Return"),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    # Generic foreign key fields
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    # object_id = models.PositiveIntegerField(null=True)
    # source_object = GenericForeignKey("content_type", "object_id")

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

    def get_remaining_balance(self, tenant):
        total_purchases_made = (
            PurchaseInvoice.objects.filter(
                tenant=tenant,
                supplier=self.pk,
            ).aggregate(
                total=Sum("total_amount")
            )["total"]
            or 0
        )

        total_payments_made = (
            PaymentMade.objects.filter(tenant=tenant, supplier=self.pk).aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )

        return total_purchases_made - total_payments_made


class PurchaseInvoice(TenantAwareModel, BaseModelMixin):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    invoice_number = models.CharField(
        verbose_name="Purchase Invoice Number",
        null=True,
        blank=True,
        max_length=100,
    )
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    received_date = models.DateTimeField(blank=True, null=True)
    order_date = models.DateTimeField(blank=True, null=True)

    returned = models.BooleanField(default=False, verbose_name="Returned Items")
   
    objects = ReturnManagers()
    all = models.Manager()

    def __str__(self):
        return f"Purchase #{self.id} - {self.supplier.name}"

    def calculate_lead_time(self) -> Optional[timedelta]:
        if self.order_date and self.received_date:
            return self.received_date - self.order_date
        return None


class PurchaseItem(TenantAwareModel, BaseModelMixin):
    purchase = models.ForeignKey(
        PurchaseInvoice,
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


#################################
##prchase return helpers#########
#################################


class PurchaseReturn(TenantAwareModel, BaseModelMixin):
    purchase_invoice = models.ForeignKey(PurchaseInvoice, on_delete=models.CASCADE)
    return_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Purchase Return #{self.id} for Invoice #{self.purchase_invoice.id}"


@receiver(post_save, sender=PurchaseReturn)
def handle_purchase_return_stock_movement(sender, instance, created, **kwargs):
    ic(sender, instance)
    if created:
        for item in instance.items.all():
            StockMovement.objects.create(
                product=item.product,
                movement_type="OUT PURCHASE RETURN",
                quantity=item.quantity,
                description=f"Purchase Return #{instance.id}",
            )
            item.product.stock_quantity -= item.quantity
            item.product.save()


@receiver(post_save, sender=PurchaseReturn)
def update_purchase_invoice_after_return(sender, instance, created, **kwargs):
    ic(sender, instance)
    if created:
        invoice = instance.purchase_invoice
        invoice.total_amount -= instance.total_amount
        invoice.save()


class PurchaseReturnItem(TenantAwareModel, BaseModelMixin):
    purchase_return = models.ForeignKey(
        PurchaseReturn, related_name="items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total(self):
        return self.price * self.quantity
