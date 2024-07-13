from django.db import models


class BaseModelMixin(models.Model):
    created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True)
    updated_at = models.DateField(verbose_name="Updated at", auto_now=True)

    class Meta:
        abstract = True
