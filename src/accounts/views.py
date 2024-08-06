from .models import BankAccount, CashAccount

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def accounts(request):
    bank_accounts = BankAccount.objects.filter(tenant=request.tenant)
    cash_accounts = CashAccount.objects.filter(tenant=request.tenant)
    context = {
        "bank_accounts": bank_accounts,
        "cash_accounts": cash_accounts,
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
