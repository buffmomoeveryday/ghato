from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from tenant.models import TenantAwareModel

from .managers import CustomUserManager


class CustomUser(AbstractUser, TenantAwareModel):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(null=True, max_length=255)
    last_name = models.CharField(null=True, max_length=255)

    is_company_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
