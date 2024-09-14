from ninja import Schema, FilterSchema
from ninja import ModelSchema
from pydantic import Field

from datetime import date, datetime, time, timedelta
from decimal import Decimal

from typing import List, Optional

from pydantic import validator

from .models import PurchaseInvoice, PurchaseItem, Supplier
from accounts.models import BankAccount, CashAccount
from sales.models import PaymentReceived
from purchases.models import PaymentMade


class PurchaseInvoiceOutSchema(ModelSchema):
    class Meta:
        model = PurchaseInvoice
        exclude = ["tenant"]


class NoPurchaseFoundSchema(Schema):
    message: str


class PurchaseInvoiceCreateSchema(Schema):
    supplier: int
    invoice_number: str
    purchase_date: datetime
    total_amount: Decimal = Field(max_digits=10, decimal_places=2)
    received_date: datetime
    order_date: datetime = None


class PurchaseInvoiceFilterSchema(Schema):
    invoice_number: Optional[str] = None
    purchase_date_from: Optional[datetime] = None
    purchase_date_to: Optional[datetime] = None
    total_amount_min: Optional[float] = None
    total_amount_max: Optional[float] = None

    def filter(self, queryset):
        if self.invoice_number:
            queryset = queryset.filter(invoice_number__icontains=self.invoice_number)
        if self.purchase_date_from:
            queryset = queryset.filter(purchase_date__gte=self.purchase_date_from)
        if self.purchase_date_to:
            queryset = queryset.filter(purchase_date__lte=self.purchase_date_to)
        if self.total_amount_min:
            queryset = queryset.filter(total_amount__gte=self.total_amount_min)
        if self.total_amount_max:
            queryset = queryset.filter(total_amount__lte=self.total_amount_max)
        return queryset


class SupplierOutSchema(ModelSchema):
    class Meta:
        model = Supplier
        exclude = ["tenant"]


class UnitOfMeasurementsSchema(Schema):
    id: int
    name: str
    field: Optional[str]


class ProductSchema(Schema):
    id: int
    name: str
    uom: Optional[UnitOfMeasurementsSchema]
    sku: str
    stock_quantity: Optional[float]
    opening_stock: Optional[int]


class PurchaseItemSchema(Schema):
    id: int
    product: ProductSchema
    quantity: int
    price: float


class PurchaseInvoiceDetailOutSchema(Schema):
    id: int
    supplier: SupplierOutSchema
    invoice_number: Optional[str]
    purchase_date: datetime
    total_amount: float
    received_date: Optional[datetime]
    order_date: Optional[datetime]
    items: List[PurchaseItemSchema]  # This will hold the list of purchase items


class BankOutSchema(ModelSchema):
    class Meta:
        model = BankAccount
        exclude = ["tenant"]


class PaymentMadeOutSchema(ModelSchema):
    class Meta:
        model = PaymentMade
        exclude = ["tenant"]


class PaymentReceivedSchema(ModelSchema):
    class Meta:
        model = PaymentReceived
        exclude = ['tenant']