from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django_htmx.http import HttpResponseClientRedirect
from icecream import ic

from .models import Product, PurchaseInovice, PurchaseItem, Supplier, UnitOfMeasurements
from .tasks import add_to_stock


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = PurchaseInovice
        fields = ["supplier", "total_amount", "received_date"]


class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ["product", "quantity", "price"]


@login_required
def purchase_index(request):

    if request.method == "GET":
        purchases = PurchaseInovice.objects.filter(tenant=request.tenant)
        context = {
            "purchases": purchases,
        }
        return render(
            request=request,
            template_name="purchase/purchase_index.html",
            context=context,
        )


@login_required
def purchase_add(request):
    context = {}
    return render(
        request=request,
        template_name="purchase/purchase_add.html",
        context=context,
    )


@login_required
def purchase_detail(request, id):
    if request.method == "GET":
        purchase = PurchaseInovice.objects.get(id=id, tenant=request.tenant)
        purchase_items = PurchaseItem.objects.filter(purchase=purchase)
        context = {
            "purchase": purchase,
            "purchase_items": purchase_items,
        }
        return render(
            request=request,
            template_name="inventory/inventory.html",
            context=context,
        )
