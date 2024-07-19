from django.db import models


class BankAccount(models.Model):

    class AccountType(models.TextChoices):
        CURRENT = "1", "CURRENT"
        SAVING = "2", "SAVING"

    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=25, decimal_places=2)
    type = models.CharField(
        max_length=25,
        choices=AccountType.choices,
        default=AccountType.CURRENT,
    )

    def transfer_to_cash(self):
        pass

    def transfer_to_bank(self):
        pass

    @property
    def balance(self):
        return self.balance


class CashAccount(models.Model):
    name = models.CharField(max_length=255, null=True)
    balance = models.DecimalField(max_digits=25, decimal_places=2)

    def transfer_to_cash(self):
        pass

    def transfer_to_bank(self):
        pass

    @property
    def balance(self):
        return self.balance


class Account(models.Model):
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=25, decimal_places=2)

    @property
    def balance(self):
        return self.balance
