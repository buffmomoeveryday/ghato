import django_filters

from .models import PurchaseInvoice, Supplier, PurchaseItem
from .models import *
from users.models import CustomUser


class PurchaseFilter(django_filters.FilterSet):
    tenant = None

    supplier__name = django_filters.CharFilter(
        field_name="supplier__name",
        lookup_expr="icontains",
        label="Supplier Name",
    )

    class Meta:
        model = PurchaseInvoice
        fields = "__all__"
        exclude = [
            "tenant",
            "created_at",
            "updated_at",
        ]

    def __init__(self, *args, **kwargs):
        self.tenant = kwargs.pop("tenant", None)
        super().__init__(*args, **kwargs)
        if self.tenant:
            self.queryset = self.queryset.filter(tenant=self.tenant)
            self.filters["supplier"].field.queryset = self.get_supplier_queryset()

    def get_supplier_queryset(self):
        return Supplier.objects.filter(tenant=self.tenant)


class InventoryFilter(django_filters.FilterSet):

    tenant = None

    class Meta:
        model = PurchaseItem
        fields = "__all__"
        exclude = [
            "tenant",
            "created_at",
            "updated_at",
        ]

    def __init__(self, *args, **kwargs):
        self.tenant = kwargs.pop("tenant", None)
        super().__init__(*args, **kwargs)

        if self.tenant:
            self.queryset = self.queryset.filter(tenant=self.tenant)

            self.filters["product"].field.queryset = self.get_queryset(
                queryset_name="products"
            )
            self.filters["purchase"].field.queryset = self.get_queryset(
                queryset_name="purchase_invoice"
            )
            self.filters["created_by"].field.queryset = self.get_queryset(
                queryset_name="user"
            )

    def get_queryset(self, queryset_name):

        user = CustomUser.objects.filter(tenant=self.tenant)
        purchase_invoice = PurchaseInvoice.objects.filter(
            tenant=self.tenant
        ).select_related("tenant", "supplier")

        products = Product.objects.filter(tenant=self.tenant).select_related(
            "created_by", "uom"
        )

        if queryset_name == "user":
            return user

        if queryset_name == "purchase_invoice":
            return purchase_invoice

        if queryset_name == "products":
            return products

        else:
            return user
