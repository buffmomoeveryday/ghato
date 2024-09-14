from django.test import TestCase
from django.test import TestCase, RequestFactory

from django.urls import reverse
from django.urls import reverse

from django.utils import timezone

from django.http import Http404
from django.http import Http404

from decimal import Decimal

from sales.models import PaymentReceived, SalesInvoice, SalesItem, Customer
from tenant.models import TenantModel
from users.models import CustomUser
from sales.models import Customer
from purchases.models import Product
from tenant.models import TenantModel as Tenant


from sales.views import (
    sales_add,
    sales_all,
    sales_detail,
    sales_invoice,
    payments_received,
)


class PaymentsReceivedViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            password="testpassword",
            email="test@user.com",
        )
        self.tenant = TenantModel.objects.create(name="Test Tenant")

        self.user.tenant = self.tenant
        self.user.save()

        self.payment1 = PaymentReceived.objects.create(
            tenant=self.tenant,
            amount=100,
            payment_date=timezone.now() - timezone.timedelta(days=1),
            customer_id=self.user.id,
        )
        self.payment2 = PaymentReceived.objects.create(
            tenant=self.tenant,
            amount=150,
            payment_date=timezone.now(),
            customer_id=self.user.id,
        )

        self.client.login(email="test@user.com", password="testpassword")

    def test_payments_received_view(self):
        response = self.client.get(reverse("payments_received"))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "payments/payments_received.html")

        self.assertIn("payments_received", response.context)
        self.assertEqual(len(response.context["payments_received"]), 2)

        self.assertIn("total_payments_received", response.context)
        self.assertEqual(response.context["total_payments_received"], 250)

        self.assertIn("last_payment", response.context)
        self.assertEqual(response.context["last_payment"], self.payment2.payment_date)


class SalesViewsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            email="test@email.com",
            password="12345",
        )
        self.tenant = Tenant.objects.create(name="Test Tenant")
        self.customer = Customer.objects.create(
            first_name="Test",
            last_name="Customer",
            tenant=self.tenant,
        )
        self.product = Product.objects.create(name="Test Product", tenant=self.tenant)

    def test_sales_add_view(self):
        request = self.factory.get(reverse("sales_add"))
        request.user = self.user
        request.tenant = self.tenant
        response = sales_add(request)
        self.assertEqual(response, {})

    def test_payments_received_view(self):
        PaymentReceived.objects.create(
            tenant=self.tenant, amount=Decimal("100.00"), payment_date="2023-01-01"
        )
        PaymentReceived.objects.create(
            tenant=self.tenant, amount=Decimal("200.00"), payment_date="2023-01-02"
        )

        request = self.factory.get(reverse("payments_received"))
        request.user = self.user
        request.tenant = self.tenant

        response = payments_received(request)

        self.assertEqual(len(response["payments_received"]), 2)
        self.assertEqual(response["total_payments_received"], Decimal("300.00"))
        self.assertEqual(response["last_payment"].strftime("%Y-%m-%d"), "2023-01-02")

    def test_sales_all_view(self):
        sales = SalesInvoice.objects.create(
            tenant=self.tenant, sales=self.customer, total_amount=Decimal("100.00")
        )
        SalesItem.objects.create(
            tenant=self.tenant,
            sales=sales,
            product=self.product,
            quantity=1,
            vat_amount=Decimal("10.00"),
        )

        request = self.factory.get(reverse("sales_all"))
        request.user = self.user
        request.tenant = self.tenant

        response = sales_all(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales/sales_list.html")
        self.assertEqual(len(response.context["sales_invoice"]), 1)
        self.assertEqual(
            response.context["sales_invoice"][0].total_vat, Decimal("10.00")
        )
        self.assertEqual(
            response.context["sales_invoice"][0].with_vat, Decimal("110.00")
        )

    def test_sales_detail_view(self):
        sales = SalesInvoice.objects.create(
            tenant=self.tenant, sales=self.customer, total_amount=Decimal("100.00")
        )
        SalesItem.objects.create(
            tenant=self.tenant,
            sales=sales,
            product=self.product,
            quantity=2,
            vat_amount=Decimal("10.00"),
        )

        request = self.factory.get(
            reverse("sales_detail", kwargs={"sales_id": sales.id})
        )
        request.user = self.user
        request.tenant = self.tenant

        response = sales_detail(request, sales.id)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales/sales_detail.html")
        self.assertEqual(response.context["sale_invoice"], sales)
        self.assertEqual(len(response.context["sale_items"]), 1)
        self.assertEqual(response.context["items"], [2])
        self.assertEqual(response.context["products"], ["Test Product"])

    def test_sales_detail_view_404(self):
        request = self.factory.get(reverse("sales_detail", kwargs={"sales_id": 999}))
        request.user = self.user
        request.tenant = self.tenant

        with self.assertRaises(Http404):
            sales_detail(request, 999)
