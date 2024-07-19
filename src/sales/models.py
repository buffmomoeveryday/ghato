from django.db import models
from tenant.models import TenantAwareModel
from core.models import BaseModelMixin
from purchases.models import Product


class Customer(TenantAwareModel, BaseModelMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Sales(TenantAwareModel, BaseModelMixin):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.id}"


class SalesInvoice(TenantAwareModel, BaseModelMixin):
    order = models.OneToOneField(Sales, on_delete=models.CASCADE)
    billing_address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ("Paid", "Paid"),
            ("Unpaid", "Unpaid"),
        ],
        default="Unpaid",
    )

    def __str__(self):
        return f"Invoice #{self.id} - {self.payment_status}"


class SalesItem(TenantAwareModel, BaseModelMixin):
    order = models.ForeignKey(Sales, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total(self):
        return self.price * self.quantity


class PaymentReceived(TenantAwareModel, BaseModelMixin):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment #{self.id} - {self.order.id}"
