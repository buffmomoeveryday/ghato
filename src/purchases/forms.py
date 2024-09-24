from django import forms

from .models import PurchaseInvoice, PurchaseItem, Supplier


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = PurchaseInvoice
        fields = ["supplier", "total_amount", "received_date"]


class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ["product", "quantity", "price"]


class SupplierEditForm(forms.ModelForm):
    class Meta:
        model = Supplier
        exclude = ["tenant", "created_at", "updated_at", "created_by"]
