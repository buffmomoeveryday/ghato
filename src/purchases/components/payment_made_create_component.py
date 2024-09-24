from django.db import transaction

from django_unicorn.components import UnicornView

from purchases.models import Supplier
from accounts.models import BankAccount, CashAccount
from purchases.models import PaymentMade
from datetime import date
from icecream import ic
from django.contrib import messages

from django.core.exceptions import ValidationError
from decimal import Decimal


class PaymentMadeCreateComponentView(UnicornView):
    template_name = "payment_made_create_component.html"

    supplier_list = []
    bank_list = []
    cash_list = []

    bank_id: str = ""
    cash_id: str = ""

    selected_supplier: str = ""
    supplier_remaining_balance: float = 0.00
    bank_balance: float = 0.00
    cash_balance: float = 0.00

    payment_date: date = date.today()
    amount: Decimal = 0.00

    transaction_id: str = ""

    cash: bool = False

    def get_bank_balance(self):
        bank = BankAccount.objects.filter(
            tenant=self.request.tenant,
            id=self.bank_id,
        ).first()

        self.bank_balance = bank.get_balance

    def get_cash_balance(self):
        cash = CashAccount.objects.filter(
            tenant=self.request.tenant,
            id=self.cash_id,
        ).first()
        self.cash_balance = cash.get_balance

    def check_supplier_remaining_balance(self):
        supplier = Supplier.objects.filter(
            id=self.selected_supplier,
            tenant=self.request.tenant,
        ).first()

        if supplier:
            self.supplier_remaining_balance = supplier.get_remaining_balance(
                tenant=self.request.tenant
            )

    def make_payment(self):
        from datetime import date

        if float(self.amount) <= 0.00:
            messages.error(self.request, "Amount cannot be less than 0 or 0")
            raise ValidationError(
                {"amount": "Amount cannot be less than 0 or 0"}, code="invalid"
            )

        if self.payment_date > date.today():
            messages.error(self.request, "Payment Date cannot be in future")
            raise ValidationError(
                {"payment_date": "Date Cannot be in future"}, code="invalid"
            )

        with transaction.atomic():
            try:
                supplier = Supplier.objects.get(
                    id=self.selected_supplier,
                    tenant=self.request.tenant,
                )
                payment_method = "Cash" if self.cash else "Bank"
                payment = PaymentMade.objects.create(
                    tenant=self.request.tenant,
                    supplier=supplier,
                    payment_method=payment_method,
                    transaction_id=self.transaction_id,
                    payment_date=self.payment_date,
                    amount=self.amount,
                )
                if self.cash:
                    cash = CashAccount.objects.get(
                        id=self.cash_id, tenant=self.request.tenant
                    )
                    cash.balance = cash.balance - self.amount
                    cash.save()
                else:
                    bank = BankAccount.objects.get(
                        id=self.bank_id, tenant=self.request.tenant
                    )
                    bank.balance = bank.balance - self.amount
                    bank.save()
                messages.success(self.request, "Created")
                self.reset()

            except Exception as e:
                messages.error(self.request, f"Some Error Occoured {e}")

    def mount(self):
        self.supplier_list = Supplier.objects.filter(tenant=self.request.tenant)
        self.bank_list = BankAccount.objects.filter(tenant=self.request.tenant)
        self.cash_list = CashAccount.objects.filter(tenant=self.request.tenant)

    def updating(self, name, value):
        ic(name, value)
