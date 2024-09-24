from django.db import models
from django.db.models import F, Sum

from core.models import BaseModelMixin
from purchases.models import Product
from tenant.models import TenantAwareModel
from .managers import ReturnManagers as SalesReturnManagers


class Customer(TenantAwareModel, BaseModelMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_balance(self):
        total = (
            Sales.objects.filter(
                customer=self,
            ).aggregate(
                total=Sum("total_amount"),
            )["total"]
            or 0
        )
        payment_received = (
            PaymentReceived.objects.filter(customer=self).aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )

        return total - payment_received

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Sales(TenantAwareModel, BaseModelMixin):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    returned = models.BooleanField(
        default=False,
    )
    objects = SalesReturnManagers()

    def __str__(self):
        return f"Order #{self.id}"


class SalesInvoice(TenantAwareModel, BaseModelMixin):
    sales = models.OneToOneField(Sales, on_delete=models.CASCADE, related_name="sales")
    billing_address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ("Paid", "Paid"),
            ("Unpaid", "Unpaid"),
            ("Partial", "Partial"),
        ],
        default="Unpaid",
    )

    def __str__(self):
        return f"Invoice #{self.id} - {self.payment_status}"

    def get_vat(self) -> int:
        total = sum(
            item.vat_amount for item in self.sales.items.all().select_related("sales")
        )
        return int(total)

    def get_total(self):
        return int(self.total_amount)

    def get_total_with_vat(self):
        return sum(item.total_with_vat for item in self.sales.items.all())

    def process_return(self): ...


class SalesItem(TenantAwareModel, BaseModelMixin):
    sales = models.ForeignKey(Sales, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_snapshot = models.IntegerField(null=True)
    vat = models.IntegerField(
        choices=[
            (13, 13),
            (0, 0),
        ],
        default=13,
    )

    vat_amount = models.GeneratedField(
        expression=(F("price") * F("quantity") * F("vat") / 100),
        output_field=models.DecimalField(max_digits=20, decimal_places=2),
        db_persist=True,
    )

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total(self):
        return self.price * self.quantity

    @property
    def total_with_vat(self) -> int:
        total = self.total + self.vat_amount
        return int(total)

    @property
    def stock_before_sales(self):
        return self.product.opening_stock - self.quantity


class PaymentReceived(TenantAwareModel, BaseModelMixin):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment #{self.id}"
