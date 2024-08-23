from django_unicorn.components import UnicornView
from accounts.models import BankAccount
from django.contrib import messages

from icecream import ic


class CreateBankAccountView(UnicornView):
    template_name = "create_bank_account.html"

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
        if (
            BankAccount.objects.filter(
                tenant=self.request.tenant,
                id=self.bank_id,
            )
            .exclude(id=self.bank_id)
            .exists()
        ):
            return messages.error(self.request, "Error")

        else:

            return messages.success(self.request, "Error")
            ic("halo returns")

    # self.call("initFlowbite")
    # return super().updated(name, value)

    def create_bank(self): ...
