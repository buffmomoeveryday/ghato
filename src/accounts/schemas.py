from accounts.models import BankAccount, CashAccount
from ninja import ModelSchema, Schema
from purchases.models import PaymentMade
from sales.models import PaymentReceived


class BankOutSchema(ModelSchema):
    class Meta:
        model = BankAccount
        exclude = ["tenant"]


class CashOutSchema(ModelSchema):
    class Meta:
        model = CashAccount
        exclude = ["tenant"]


class PaymentMadeOutSchema(ModelSchema):
    class Meta:
        model = PaymentMade
        exclude = ["tenant"]


class PaymentReceivedSchema(ModelSchema):
    class Meta:
        model = PaymentReceived
        exclude = ["tenant"]


class AllAccountsSchema(Schema):
    bank: BankOutSchema
    cash: CashOutSchema
