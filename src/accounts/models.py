from django.db import models
from tenant.models import TenantAwareModel
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    @property
    def get_balance(self):
        return self.balance


class CashAccount(TenantAwareModel):
    name = models.CharField(max_length=255, null=True)
    balance = models.DecimalField(max_digits=25, decimal_places=2, default=0.00)

    def transfer_to_cash(self):
        pass

    def transfer_to_bank(self):
        pass

    @property
    def get_balance(self):
        return self.balance


class Account(TenantAwareModel):
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=25, decimal_places=2, default=0.00)



@receiver(post_save,sender=BankAccount)
def bank_account_save_handler(*args,**kwargs):
    print("halo bank")
    
@receiver(post_save,sender=CashAccount)
def cash_account_save_handler(*args,**kwargs):
    print("halo cash")