from django.db import models


class TenantModel(models.Model):
    name = models.CharField(verbose_name="Tenant Name", max_length=255, unique=True)
    domain = models.CharField(verbose_name="Domain", max_length=10, unique=True)

    class Meta:
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"

    def __str__(self):
        return self.domain


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
