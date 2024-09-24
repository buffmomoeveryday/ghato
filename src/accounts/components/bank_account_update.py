from django_unicorn.components import UnicornView
from accounts.models import BankAccount
from django.contrib import messages
from django.core.exceptions import ValidationError


class BankAccountUpdateView(UnicornView):
    template_name = "bank_account_update.html"

    bank_id = None
    name: str = None
    balance: float = None
    account_type = None

    modal_id: str = None

    def mount(self):
        self.modal_id = self.component_kwargs["modal_id"]
        self.bank_id = self.component_kwargs["bank_id"]

        bank = BankAccount.objects.get(tenant=self.request.tenant, id=self.bank_id)

        self.name = bank.name
        self.balance = bank.balance
        self.account_type = bank.accounttype

    def _update(self):
        if self.balance < 0:
            messages.error(self.request, "Cant be smaller than 0")
            raise ValidationError(
                {"balance": "Balance Can't smaller than 0 "}, code="invalid"
            )

        if (
            BankAccount.objects.filter(
                tenant=self.request.tenant,
                id=self.bank_id,
            )
            .exclude(id=self.bank_id)
            .exists()
        ):

            self.parent.force_render = True
            return messages.error(self.request, "Bank Account Already Exists")

        else:
            messages.success(self.request, "Successfully Changed")

    def create_bank(self): ...
