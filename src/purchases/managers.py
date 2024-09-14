from django.db import models


class ReturnManagers(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(returned=False)

    def returned(self, tenant):
        return self.get_queryset().filter(returned=True)
