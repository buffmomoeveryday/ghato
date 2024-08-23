from django_unicorn.components import UnicornView
from datetime import date
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.db import transaction
from django.contrib import messages
from accounts.models import BankAccount, CashAccount
from sales.models import Customer, PaymentReceived, Sales


class PaymentReceivedComponentView(UnicornView):
    template_name = "payment_received_component.html"

    bank_list = []
    cash_list = []
    customer_list = []

    cash_payment: bool = True
    bank_id = None
    cash_id = None
    received_amount: float = 0.00
    customer_id = None
    payment_date: date = date.today()
    balance: float = 0.00
    transaction_id: str = None
    payment_method: str = None

    def mount(self):
        self.bank_list = BankAccount.objects.filter(tenant=self.request.tenant)
        self.cash_list = CashAccount.objects.filter(tenant=self.request.tenant)
        self.customer_list = Customer.objects.filter(tenant=self.request.tenant)
        if self.cash_payment:
            self.transaction_id = self.get_transaction_id()
        else:
            self.transaction_id = None

    def check_txn_id(self):
        txn_id = self.transaction_id
        exists = PaymentReceived.objects.filter(transaction_id=txn_id).exists()
        if exists:
            raise ValidationError(
                {"transaction_id": "The TXN id already exits"}, code="invalid"
            )

    def updated(self, name, value):
        if name == "customer_id" and self.customer_id and self.request.tenant:
            self.balance = self.get_balance(
                customer_id=self.customer_id, tenant_id=self.request.tenant.id
            )

        self.transaction_id = self.get_transaction_id()

    def get_balance(self, customer_id, tenant_id):
        balance = (
            Sales.objects.filter(
                tenant_id=tenant_id, customer_id=customer_id
            ).aggregate(total_amount=Sum("total_amount"))["total_amount"]
            or 0
        )

        payments = (
            PaymentReceived.objects.filter(
                tenant_id=tenant_id, customer_id=customer_id
            ).aggregate(total_received=Sum("amount"))["total_received"]
            or 0
        )

        return balance - payments

    def get_transaction_id(self):
        return f"TXN-{date.today().strftime('%Y%m%d%H%M%S')}"

    def validate_date(self):
        if self.payment_date > date.today():
            raise ValidationError(
                {"payment_date": "Payment date must be today or earlier."},
                code="invalid",
            )

    def add_payment(self):
        if not all(
            [
                self.customer_id,
                self.payment_method,
                self.payment_date,
                self.transaction_id,
                self.received_amount,
            ]
        ):
            messages.error(self.request, "Please fill in all required fields.")
            return
        try:
            with transaction.atomic():
                payment_received = PaymentReceived.objects.create(
                    customer_id=self.customer_id,
                    payment_method=self.payment_method,
                    payment_date=self.payment_date,
                    transaction_id=self.transaction_id,
                    amount=self.received_amount,
                    tenant=self.request.tenant,
                )

            self.customer_id = None
            self.bank_id = None
            self.cash_id = None
            self.received_amount = 0.00
            self.payment_method = None
            self.transaction_id = None
            self.payment_date = date.today()

            messages.success(self.request, "Payment added successfully.")

        except Exception as e:
            messages.error(self.request, e)
