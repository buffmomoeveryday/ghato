from django_unicorn.components import UnicornView

from tenant.models import TenantModel


class ApiComponentView(UnicornView):
    api: str = None

    def mount(self):
        self.api = self.request.tenant.api_key

    def refresh_api_key(self):
        tenant = TenantModel.objects.get(id=self.request.tenant.id)
        api = tenant.create_api()
        tenant.api_key = api
        tenant.save()
        self.api = tenant.api_key
