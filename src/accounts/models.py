from django.db import models
from tenant.models import TenantAwareModel


class BankAccount(TenantAwareModel):

    class AccountType(models.TextChoices):
        CURRENT = "1", "CURRENT"
        SAVING = "2", "SAVING"

    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=25, decimal_places=2, default=0.00)
    accounttype = models.CharField(
        max_length=25,
        choices=AccountType.choices,
        default=AccountType.CURRENT,
    )

    def transfer_to_cash(self):
        pass

    def transfer_to_bank(self):
        pass


class CashAccount(TenantAwareModel):
    name = models.CharField(max_length=255, null=True)
    balance = models.DecimalField(max_digits=25, decimal_places=2, default=0.00)

    def transfer_to_cash(self):
        pass

    def transfer_to_bank(self):
        pass


class Account(TenantAwareModel):
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=25, decimal_places=2, default=0.00)
