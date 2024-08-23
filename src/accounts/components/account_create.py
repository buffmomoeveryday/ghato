from django_unicorn.components import UnicornView
from accounts.models import BankAccount, CashAccount, Account
from django.contrib import messages
from decimal import Decimal

from icecream import ic


class AccountCreateView(UnicornView):
    template_name = "account_create.html"

    account_types = [
        ("bank", "Bank Account"),
        ("cash", "Cash Account"),
        ("normal", "Normal Account"),
    ]
    selected_account_type: str = "bank"

    account_name: str = ""
    account_balance: Decimal = Decimal("0.00")

    bank_account_types = BankAccount.AccountType.choices
    bank_account_type: str = BankAccount.AccountType.CURRENT

    def mount(self):
        self.reset_form()

    def create_account(self):
        ic("called")
        if not self.account_name or self.account_balance < 0:
            messages.error(
                request=self.request, message="Please fill in all fields correctly."
            )
            return

        try:
            if self.selected_account_type == "bank":
                ic("bank")
                BankAccount.objects.create(
                    name=self.account_name,
                    balance=self.account_balance,
                    accounttype=self.bank_account_type,
                    tenant=self.request.tenant,
                )
            elif self.selected_account_type == "cash":
                ic("cash")
                CashAccount.objects.create(
                    name=self.account_name,
                    balance=self.account_balance,
                    tenant=self.request.tenant,
                )
            else:
                ic("account")
                Account.objects.create(
                    name=self.account_name,
                    balance=self.account_balance,
                    tenant=self.request.tenant,
                )

            messages.success(
                request=self.request,
                message=f"{self.selected_account_type.capitalize()} account '{self.account_name}' created successfully!",
            )
            self.reset_form()

        except Exception as e:
            messages.error(request=self.request, message=f"An error occurred: {str(e)}")

    def reset_form(self):
        self.account_name = ""
        self.account_balance = Decimal("0.00")
        self.bank_account_type = BankAccount.AccountType.CURRENT
