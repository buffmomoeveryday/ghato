from django.db import models

from core.models import BaseModelMixin
from tenant.models import TenantAwareModel


class UnitOfMeasurements(TenantAwareModel, BaseModelMixin):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(TenantAwareModel, BaseModelMixin):
    name = models.CharField(max_length=100)
    uom = models.ForeignKey(
        UnitOfMeasurements,
        on_delete=models.SET_NULL,
        null=True,
    )
    sku = models.CharField(max_length=50, unique=True)

    stock_quantity = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Customer(TenantAwareModel, BaseModelMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(TenantAwareModel, BaseModelMixin):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(TenantAwareModel, BaseModelMixin):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Invoice(TenantAwareModel, BaseModelMixin):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    billing_address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=[("Paid", "Paid"), ("Unpaid", "Unpaid")],
        default="Unpaid",
    )

    def __str__(self):
        return f"Invoice #{self.id} - {self.payment_status}"


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


class Payment(TenantAwareModel, BaseModelMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Payment #{self.id} - {self.order.id}"


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
