from django.test import TestCase
from tenant.models import TenantModel

from django.utils import timezone
from .middlewares import TenantMiddleware


from django.test import TestCase
from unittest.mock import Mock, patch
from django.http import HttpResponseRedirect


class TenantModelTestCase(TestCase):
    def setUp(self):
        self.tenant = TenantModel.objects.create(
            name="Test Tenant", domain="testtenant"
        )

    def test_tenant_creation(self):
        self.assertEqual(self.tenant.name, "Test Tenant")
        self.assertEqual(self.tenant.domain, "testtenant")

    def test_create_api(self):
        api_key = self.tenant.create_api()
        self.assertEqual(len(api_key), 20)

    def test_tenant_update(self):
        self.tenant.name = "Updated Tenant"
        self.tenant.save()
        self.tenant.refresh_from_db()
        self.assertEqual(self.tenant.name, "Updated Tenant")

    def test_tenant_delete(self):
        tenant_id = self.tenant.id
        self.tenant.delete()
        with self.assertRaises(TenantModel.DoesNotExist):
            TenantModel.objects.get(id=tenant_id)


class TenantMiddlewareTestCase(TestCase):
    def setUp(self):
        self.middleware = TenantMiddleware(get_response=Mock())
        self.request = Mock()
        self.request.META = {
            "HTTP_PROFILE_ID": "12345",
            "HTTP_X_API_KEY": None,  # No API key initially
            "REQUEST_METHOD": "POST",
            "HTTP_USER_AGENT": "TEST",
        }
        self.request.COOKIES = {}
        self.request.path = "/"
        self.request.session = {}
        self.request.get_host.return_value = "test.example.com"

    @patch("tenant.middlewares.cache")
    @patch("tenant.middlewares.get_subdomain")
    @patch("tenant.middlewares.TenantModel.objects.filter")
    def test_tenant_retrieval_success(
        self, mock_filter, mock_get_subdomain, mock_cache
    ):
        # Mock subdomain extraction
        mock_get_subdomain.return_value = "test"

        # Simulate tenant lookup success
        tenant_mock = Mock()
        mock_filter.return_value.first.return_value = tenant_mock

        # Mock cache is empty
        mock_cache.get.return_value = None

        # Call middleware
        response = self.middleware(self.request)

        # Check if tenant is assigned to the request and cache is updated
        self.assertEqual(self.request.tenant, tenant_mock)
        mock_cache.set.assert_called_once()

    @patch("tenant.middlewares.get_subdomain")
    @patch("tenant.middlewares.TenantModel.objects.filter")
    def test_redirect_to_register_if_no_tenant(self, mock_filter, mock_get_subdomain):
        # Simulate subdomain and tenant lookup failure
        mock_get_subdomain.return_value = "test"
        mock_filter.return_value.first.return_value = None

        # Call middleware
        response = self.middleware(self.request)

        # Ensure redirect to register page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/register/")

    def test_api_key_bypass(self):
        self.request.META["HTTP_X_API_KEY"] = "valid-key"
        self.request.path = "/api/v1/resource"

        # Call middleware
        response = self.middleware(self.request)

        # Since API key is valid, no tenant logic is triggered
        self.assertEqual(response, self.middleware.get_response(self.request))

    def test_no_tenant_redirect(self):
        self.request.tenant = None
        self.request.path = "/"

        # Call middleware with no tenant
        response = self.middleware(self.request)

        # Ensure redirect to /register/
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/register/")
