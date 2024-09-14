from django.db import models
from django.db.models import Q


class ReturnManagers(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return (
            super()
            .get_queryset()
            .filter(
                returned=False,
                # Q(returned=False) | Q(returned=None),
            )
        )

    def returned(self, tenant):
        return self.get_queryset().filter(returned=True)
