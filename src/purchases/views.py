from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.shortcuts import get_object_or_404, render

from .filters import PurchaseFilter
from .models import PaymentMade, PurchaseInovice, PurchaseItem, Supplier


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
    queryset = PurchaseInovice.objects.filter(tenant=request.tenant).select_related(
        "supplier"
    )
    filter = PurchaseFilter(request.GET, queryset=queryset, tenant=request.tenant)
    context = {
        "filter": filter,
    }
    return render(request, "purchase/purchase_index.html", context)


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
        purchase = (
            PurchaseInovice.objects.filter(id=id, tenant=request.tenant)
            .select_related("supplier")
            .first()
        )
        purchase_items = PurchaseItem.objects.filter(purchase=purchase).select_related(
            "purchase", "product"
        )
        context = {
            "purchase": purchase,
            "purchase_items": purchase_items,
        }
        return render(
            request=request,
            template_name="purchase/purchase_detail.html",
            context=context,
        )


@login_required
def supplier_detail(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id, tenant=request.tenant)
    supplier_invoice = PurchaseInovice.objects.filter(
        supplier=supplier, tenant=request.tenant
    )
    payments_made = PaymentMade.objects.filter(supplier=supplier, tenant=request.tenant)
    payment_to_be_made = (
        supplier_invoice.aggregate(Sum("total_amount"))["total_amount__sum"] or 0
    )

    payments_made_amount = payments_made.aggregate(Sum("amount"))["amount__sum"] or 0
    payment_remaining = payment_to_be_made - payments_made_amount

    context = {
        "supplier": supplier,
        "supplier_invoice": supplier_invoice,
        "payment_to_be_made": payment_to_be_made,
        "payments_made_amount": payments_made_amount,
        "payment_remaining": payment_remaining,
        "payments_made": payments_made,
    }
    return render(request, "supplier/supplier_detail.html", context)


@login_required
def payments_made(request):
    payments_made = PaymentMade.objects.filter(tenant=request.tenant).select_related(
        "supplier"
    )
    total_payments_made = payments_made.aggregate(Sum("amount"))
    context = {
        "payments_made": payments_made,
        "total_payments_made": total_payments_made["amount__sum"],
    }

    return render(
        request=request, template_name="payments/payments_made.html", context=context
    )


@login_required
def inventory(request):
    tenant = request.user.tenant
    purchase_items = PurchaseItem.objects.filter(tenant=tenant).select_related(
        "product",
        "tenant",
        "purchase__supplier",
    )

    total_inventory_value = (
        purchase_items.annotate(
            total_value=ExpressionWrapper(
                F("quantity") * F("price"), output_field=DecimalField()
            )
        ).aggregate(total_value_sum=Sum("total_value"))["total_value_sum"]
        or 0
    )

    context = {
        "inventory": purchase_items,
        "total_inventory_value": total_inventory_value,
    }
    return render(
        request=request,
        template_name="inventory/inventory_index.html",
        context=context,
    )


@login_required
def product_stock_movement(request, product_id):
    pass


@login_required
def stock_movement(request):
    pass
