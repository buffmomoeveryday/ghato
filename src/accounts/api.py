from ninja import NinjaAPI
from ninja import NinjaAPI
from ninja.pagination import paginate, LimitOffsetPagination
from accounts import models
from sales.models import PaymentReceived
from purchases.models import PaymentMade

from core.utils import ApiKey
from .schemas import (
    BankOutSchema,
    PaymentMadeOutSchema,
    PaymentReceivedSchema,
    AllAccountsSchema,
)
from typing import List


accounts_api = NinjaAPI(auth=ApiKey())


@accounts_api.get("/", response={200: List[AllAccountsSchema]})
@paginate(LimitOffsetPagination)
def all_account_list(request):
    bank = models.BankAccount.objects.filter(tenant=request.auth)
    cash = models.CashAccount.objects.filter(tenant=request.auth)

    accounts: List = []

    for bank, cash in zip(bank, cash):
        accounts.append({"bank": bank, "cash": cash})

    return accounts


@accounts_api.get("bank/all", response={200: List[BankOutSchema]})
@paginate(LimitOffsetPagination)
def bank_list(request):
    bank = models.BankAccount.objects.filter(tenant=request.auth)
    return bank


@accounts_api.get("bank/{bank_id}", response={200: BankOutSchema})
def bank(request, bank_id):
    bank = models.BankAccount.objects.get(tenant=request.auth, id=bank_id)
    return bank


@accounts_api.get("payment-made/", response={200: List[PaymentMadeOutSchema]})
@paginate(LimitOffsetPagination)
def payments_made(request):
    payments = PaymentMade.objects.filter(
        tenant=request.auth,
    ).order_by(
        "-updated_at",
        "amount",
    )
    return payments


@accounts_api.get("payment-received/", response={200: List[PaymentReceivedSchema]})
@paginate(LimitOffsetPagination)
def payments_received(request):
    payments_received = PaymentReceived.objects.filter(
        tenant=request.auth,
    ).order_by("-updated_at")
    return payments_received
