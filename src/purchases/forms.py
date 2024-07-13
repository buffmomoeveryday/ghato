from django import forms

from .models import PurchaseInovice, PurchaseItem


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = PurchaseInovice
        fields = ["supplier", "total_amount", "received_date"]


class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ["product", "quantity", "price", "received_quantity"]
