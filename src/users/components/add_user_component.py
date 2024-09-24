from django_unicorn.components import UnicornView
from pydantic import EmailStr
from tenant.models import TenantModel
from users.models import CustomUser
from icecream import ic
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db import transaction


class AddUserComponentView(UnicornView):
    email: EmailStr = None
    first_name: str = ""
    last_name: str = ""
    password: str = ""

    employees = []

    @transaction.atomic()
    def create_user(self):
        ic(self.email, self.first_name, self.last_name, self.password)
        if (
            not self.email
            or not self.first_name
            or not self.last_name
            or not self.password
        ):
            messages.error(self.request, "Please Fill Up all the form fields")
            return

        if CustomUser.objects.filter(email=self.email):
            messages.error(self.request, "User Already Exists")
            return

        try:
            user = CustomUser.objects.create(
                email=self.email,
                password=make_password(password=self.password),
                first_name=self.first_name,
                last_name=self.last_name,
                is_company_admin=False,
                tenant=self.request.tenant,
            )
            user.save()
            self.employees = CustomUser.objects.filter(
                tenant=self.request.tenant
            ).exclude(id=self.request.user.id)

        except Exception as e:
            messages.error(self.request, e)

        self.email = ""
        self.password = ""

        self.first_name = ""
        self.last_name = ""

        messages.success(self.request, "User Created Successfully")

    def mount(self):
        self.employees = CustomUser.objects.filter(
            tenant=self.request.tenant,
        ).exclude(id=self.request.user.id)

    class Meta: ...
