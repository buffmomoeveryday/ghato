from django.test import TestCase
from django.urls import reverse

# from django.contrib.auth.models import User
from .models import PaymentReceived
from tenant.models import TenantModel
from django.utils import timezone
from users.models import CustomUser as User


class PaymentsReceivedViewTest(TestCase):
    def setUp(self):
        # Create a user and a tenant
        self.user = User.objects.create_user(
            password="testpassword",
            email="test@user.com",
        )
        self.tenant = TenantModel.objects.create(name="Test Tenant")

        # Add the tenant to the user's profile or tenant relationship if necessary
        # Assuming the user has a tenant attribute
        self.user.tenant = self.tenant
        self.user.save()

        # Create some payment records for the tenant
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

        # Log in the user
        self.client.login(username="testuser", password="testpassword")

    def test_payments_received_view(self):
        # Perform a GET request to the view
        response = self.client.get(reverse("payments_received"))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the correct template was used
        self.assertTemplateUsed(response, "payments/payments_received.html")

        # Check that the payments are in the context
        self.assertIn("payments_received", response.context)
        self.assertEqual(len(response.context["payments_received"]), 2)

        # Check that the total payments received is correct
        self.assertIn("total_payments_received", response.context)
        self.assertEqual(response.context["total_payments_received"], 250)

        # Check that the last payment date is correct
        self.assertIn("last_payment", response.context)
        self.assertEqual(response.context["last_payment"], self.payment2.payment_date)


# Create your tests here.
