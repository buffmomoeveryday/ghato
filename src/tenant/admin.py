from django.contrib import admin

# Register your models here.
from .models import TenantModel

admin.site.register(TenantModel)
