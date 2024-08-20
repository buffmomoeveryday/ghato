from .models import BankAccount, CashAccount
from purchases.models import PaymentMade
from sales.models import PaymentReceived

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import collections

from django.db.models import Sum, CharField, Value

from icecream import ic


@login_required
def accounts(request):

    bank_accounts = BankAccount.objects.filter(tenant=request.tenant)
    cash_accounts = CashAccount.objects.filter(tenant=request.tenant)

    bank_balance = bank_accounts.aggregate(balance=Sum("balance"))["balance"] or 0
    cash_balance = cash_accounts.aggregate(balance=Sum("balance"))["balance"] or 0

    payment_made = PaymentMade.objects.filter(tenant=request.tenant)
    payment_received = PaymentReceived.objects.filter(tenant=request.tenant)

    recent_transactions = list(
        payment_made.values("payment_date", "amount", "payment_method").annotate(
            transaction_type=Value("made", output_field=CharField())
        )[:2]
    ) + list(
        payment_received.values("payment_date", "amount", "payment_method").annotate(
            transaction_type=Value("received", output_field=CharField()),
        )[:2]
    )
    sorted_transaction = sorted(
        recent_transactions, key=lambda x: x["payment_date"], reverse=True
    )

    context = {
        "bank_accounts": bank_accounts,
        "cash_accounts": cash_accounts,
        "total_balance": cash_balance + bank_balance,
        "bank_balance": bank_balance,
        "cash_balance": cash_balance,
        "recent_transactions": sorted_transaction,
    }

    return render(
        request,
        template_name="accounts/bank_list.html",
        context=context,
    )


@login_required
def create_accounts(request):
    if request.method == "POST":
        pass
    return render(request=request, template_name="accounts/create.html")
