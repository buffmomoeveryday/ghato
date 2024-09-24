from django.db import models
import random
import string
from django.core.validators import integer_validator
from django.core.exceptions import ValidationError
import re


def validate_domain_name(value):
    num_format = re.compile("^-?\d+(\.\d+)?$")
    isnumber = re.match(num_format, value)
    if isnumber:
        raise ValidationError(
            message="The Domain Name Cannot be numeric",
        )


class TenantModel(models.Model):
    name = models.CharField(verbose_name="Tenant Name", max_length=255, unique=True)
    domain = models.CharField(
        verbose_name="Domain",
        max_length=10,
        unique=True,
        validators=[validate_domain_name],
    )
    api_key = models.CharField(
        verbose_name="API Key", max_length=20, unique=True, blank=True, null=True
    )

    class Meta:
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"

    def __str__(self):
        return self.domain

    def create_api(self, length=20):
        letters_and_digits = string.ascii_letters + string.digits
        result_str = "".join((random.choice(letters_and_digits) for i in range(length)))
        return result_str


class TenantAwareQuerySet(models.QuerySet):
    def filter_by_tenant(self, tenant):
        return self.filter(tenant=tenant)


class TenantAwareManager(models.Manager):
    def get_queryset(self):
        return TenantAwareQuerySet(self.model, using=self._db)

    def filter_by_tenant(self, tenant):
        return self.get_queryset().filter_by_tenant(tenant)


class TenantAwareModel(models.Model):
    tenant = models.ForeignKey(
        TenantModel,
        on_delete=models.CASCADE,
        related_name="%(class)s_instances",
        null=True,
    )

    objects = TenantAwareManager()

    class Meta:
        abstract = True
