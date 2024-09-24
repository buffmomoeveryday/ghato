from django.contrib import admin

from .models import TenantModel


@admin.register(TenantModel)
class TenantModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "domain", "api_key")
    search_fields = ("name",)
