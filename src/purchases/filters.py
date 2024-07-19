import django_filters
from django import forms
from .models import PurchaseInovice, Supplier


class PurchaseFilter(django_filters.FilterSet):
    tenant = None

    supplier__name = django_filters.CharFilter(
        field_name="supplier__name",
        lookup_expr="icontains",
        label="Supplier Name",
    )

    class Meta:
        model = PurchaseInovice
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
