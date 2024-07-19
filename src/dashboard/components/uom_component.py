from django_unicorn.components import UnicornView
from purchases.models import UnitOfMeasurements
from typing import List
from icecream import ic
from django.contrib import messages
from django.db import transaction


class UomComponentView(UnicornView):
    template_name = "unicorn/uom_component.html"

    uoms: List = []
    new_uom: str = ""

    editing_uom: str = ""
    editing_uom_id: int = None
    editing = False

    def add_new_uom(self):
        if self.new_uom == "":
            messages.error(self.request, "Cannot be empty")
            return

        _, created = UnitOfMeasurements.objects.get_or_create(
            name=self.new_uom.lower(),
            tenant=self.request.tenant,
        )

        if created:
            self.uoms = UnitOfMeasurements.objects.filter(tenant=self.request.tenant)
            messages.success(self.request, "Success")
            self.new_uom = ""

        else:
            messages.error(self.request, "Already exists")

    @transaction.atomic()
    def delete_uom(self, uom_id):
        uoms = UnitOfMeasurements.objects.filter(tenant=self.request.tenant, id=uom_id)
        uoms.delete()
        self.uoms = []
        self.uoms = UnitOfMeasurements.objects.filter(tenant=self.request.tenant)
        messages.success(self.request, "Successfully deleted")

    def edit(self, uom_id):
        self.editing = True
        self.editing_uom_id = uom_id

        editing_uom = UnitOfMeasurements.objects.get(
            tenant=self.request.tenant,
            id=uom_id,
        )

        self.editing_uom = editing_uom.name

    @transaction.atomic()
    def update_uom(self):
        ic("update_uom called")
        ic(self.editing_uom_id, self.editing_uom)

        if self.editing_uom == "":
            messages.error(self.request, "Cannot be empty")
            return

        try:
            uom = UnitOfMeasurements.objects.get(
                id=self.editing_uom_id, tenant=self.request.tenant
            )
            uom.name = self.editing_uom.lower()
            uom.save()
            ic("UOM updated")

            self.uoms = UnitOfMeasurements.objects.filter(tenant=self.request.tenant)
            messages.success(self.request, "Successfully updated")
            self.editing = False
            self.editing_uom = ""
            self.editing_uom_id = None
            self.call("refresh_component")
        except UnitOfMeasurements.DoesNotExist:
            messages.error(self.request, "UOM not found")
            ic("UOM not found")

    def mount(self):
        uoms = UnitOfMeasurements.objects.filter(tenant=self.request.tenant)
        self.uoms = uoms

    def updated(self, name, value):
        ic(name, value)
        ic("update called")
