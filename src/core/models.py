from django.db import models
from users.models import CustomUser


class BaseModelMixin(models.Model):
    created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Updated at", auto_now=True)
    created_by = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
