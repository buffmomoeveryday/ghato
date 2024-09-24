from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from purchases.models import Product, PurchaseInvoice, PurchaseItem
from sales.models import Sales, SalesItem, PaymentReceived, Customer
from purchases.models import PaymentMade, Supplier
from tenant.models import TenantModel as Tenant
from django.test.utils import override_settings
from unittest.mock import patch
from django.conf import settings

from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from .views import dashboard_index

User = get_user_model()


class DashboardIndexViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        # Create a tenant
        self.tenant = Tenant.objects.create(name="Test Tenant", domain="test")

        # Create a user and assign the tenant
        self.user = User.objects.create_user(email="test@user", password="password")
        self.user.tenant = self.tenant
        self.user.save()

        # Create customer and supplier
        self.customer = Customer.objects.create(
            first_name="Hello",
            last_name="Baby",
            email="hello@baby",
            phone_number="12345678",
            address="Hello Baby",
            tenant=self.tenant,
        )
        self.supplier = Supplier.objects.create(
            name="Hello",
            contact_person="Baby",
            email="hello@baby",
            phone_number="123456789",
            address="Hello",
            tenant=self.tenant,
        )

        # Create some dummy data
        self.product = Product.objects.create(
            name="Test Product",
            sku="SKU123",
            stock_quantity=100,
            opening_stock=50,
            tenant=self.tenant,
        )

        self.sales = Sales.objects.create(
            customer=self.customer,
            total_amount=200,
            returned=False,
            tenant=self.tenant,
        )
        self.sales_item = SalesItem.objects.create(
            sales=self.sales,
            product=self.product,
            quantity=2,
            price=100,
            tenant=self.tenant,
        )

        self.purchase_invoice = PurchaseInvoice.objects.create(
            supplier=self.supplier,
            total_amount=500,
            tenant=self.tenant,
        )
        self.purchase_item = PurchaseItem.objects.create(
            purchase=self.purchase_invoice,
            product=self.product,
            quantity=10,
            price=50,
            tenant=self.tenant,
        )

        self.payment_received = PaymentReceived.objects.create(
            amount=200,
            transaction_id="TRX123",
            customer=self.customer,
            tenant=self.tenant,
        )
        self.payment_made = PaymentMade.objects.create(
            amount=100,
            transaction_id="TRX456",
            supplier=self.supplier,
            tenant=self.tenant,
        )

    def setup_request(self, url):
        request = self.factory.get(url)
        request.tenant = self.tenant
        request.user = self.user

        # Add session
        session_middleware = SessionMiddleware(lambda x: None)
        session_middleware.process_request(request)
        request.session.save()

        # Add authentication
        auth_middleware = AuthenticationMiddleware(lambda x: None)
        auth_middleware.process_request(request)

        return request

    @override_settings(
        MIDDLEWARE=[
            mw for mw in settings.MIDDLEWARE if not mw.endswith("TenantMiddleware")
        ]
    )
    def test_dashboard_index_view(self):
        request = self.setup_request(reverse("dashboard_index"))

        response = dashboard_index(request)

        # Check the response status
        self.assertEqual(response.status_code, 200)

        # Debug: Print context keys
        if hasattr(response, "context_data"):
            print(
                f"Context keys: {response.context_data.keys() if response.context_data else 'No context'}"
            )
        else:
            print("Response has no context_data attribute")

        # Check if context data exists
        self.assertIsNotNone(response.context_data)
        self.assertIn("total_sales_made", response.context_data)
        self.assertIn("profit", response.context_data)
        self.assertIn("top_selling_products_data", response.context_data)

        # Validate some of the calculated data
        self.assertEqual(response.context_data["total_sales_made"], 200)
        self.assertEqual(response.context_data["total_purchase_made"], 500)
        self.assertEqual(response.context_data["total_stock_remaining"], 100)
        self.assertEqual(response.context_data["total_payments_made"], 100)
        self.assertEqual(response.context_data["total_payments_received"], 200)

        cogs = (
            response.context_data["total_purchase_made"]
            - response.context_data["total_stock_remaining"]
        )
        self.assertEqual(
            response.context_data["profit"],
            response.context_data["total_sales_made"] - cogs,
        )

        # Validate JSON data for top-selling products
        top_selling_products = response.context_data["top_selling_products_data"]
        self.assertIn(self.product.name, top_selling_products)

        # Check customer purchases data
        customer_purchases = response.context_data["customer_purchases_data"]
        self.assertIn(
            f"{self.customer.first_name} {self.customer.last_name}", customer_purchases
        )

    @override_settings(
        MIDDLEWARE=[
            mw for mw in settings.MIDDLEWARE if not mw.endswith("TenantMiddleware")
        ]
    )
    def test_dashboard_view_with_no_data(self):
        # Clear existing data for no data scenario
        Sales.objects.all().delete()
        PurchaseInvoice.objects.all().delete()
        PaymentReceived.objects.all().delete()
        PaymentMade.objects.all().delete()

        request = self.setup_request(reverse("dashboard_index"))

        response = dashboard_index(request)

        # Check the response status
        self.assertEqual(response.status_code, 200)

        # Debug: Print context keys
        if hasattr(response, "context_data"):
            print(
                f"Context keys: {response.context_data.keys() if response.context_data else 'No context'}"
            )
        else:
            print("Response has no context_data attribute")

        # Ensure that zero values are returned when there's no data
        self.assertIsNotNone(response.context_data)
        self.assertEqual(response.context_data["total_sales_made"], 0)
        self.assertEqual(response.context_data["total_purchase_made"], 0)
        self.assertEqual(response.context_data["total_stock_remaining"], 0)
        self.assertEqual(response.context_data["total_payments_made"], 0)
        self.assertEqual(response.context_data["total_payments_received"], 0)
        self.assertEqual(response.context_data["profit"], 0)
