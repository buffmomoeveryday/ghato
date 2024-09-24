from decimal import Decimal
from django.test import TestCase
from django.db.models import Sum
from datetime import timedelta

from .models import (
    Customer,
    Sales,
    SalesInvoice,
    SalesItem,
    PaymentReceived,
    Product,
)

from purchases.models import (
    StockMovement,
    UnitOfMeasurements,
    PaymentMade,
    Supplier,
    PurchaseInvoice,
    PurchaseItem,
    PurchaseReturn,
    PurchaseReturnItem,
)
from tenant.models import TenantModel


class CustomerTest(TestCase):
    def setUp(self):
        self.tenant = TenantModel.objects.create(
            name="Test Tenant", domain="testdomain"
        )
        self.customer = Customer.objects.create(
            tenant=self.tenant,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="123456789",
            address="123 Main St",
        )
        self.sales = Sales.objects.create(
            tenant=self.tenant, customer=self.customer, total_amount=Decimal("100.00")
        )
        self.payment = PaymentReceived.objects.create(
            tenant=self.tenant,
            amount=Decimal("50.00"),
            payment_method="Credit Card",
            transaction_id="1234567890",
            customer=self.customer,
        )

    def test_customer_full_name(self):
        self.assertEqual(self.customer.get_full_name, "John Doe")

    def test_customer_balance(self):
        balance = self.customer.get_balance
        expected_balance = Decimal("100.00") - Decimal("50.00")
        self.assertEqual(balance, expected_balance)


class SalesTest(TestCase):
    def setUp(self):
        self.tenant = TenantModel.objects.create(
            name="Test Tenant", domain="testdomain"
        )
        self.product = Product.objects.create(
            tenant=self.tenant,
            name="Test Product",
            uom=UnitOfMeasurements.objects.create(name="Unit", field="FLOAT"),
            sku="TEST123",
            stock_quantity=100.0,
            opening_stock=50,
        )
        self.customer = Customer.objects.create(
            tenant=self.tenant,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="123456789",
            address="123 Main St",
        )
        self.sales = Sales.objects.create(
            tenant=self.tenant, customer=self.customer, total_amount=Decimal("100.00")
        )
        self.sales_item = SalesItem.objects.create(
            tenant=self.tenant,
            sales=self.sales,
            product=self.product,
            quantity=2,
            price=Decimal("50.00"),
            stock_snapshot=10,
            vat=13,
        )

    def test_sales_str(self):
        self.assertEqual(str(self.sales), f"Order #{self.sales.id}")

    def test_sales_item_total(self):
        self.assertEqual(self.sales_item.total, Decimal("100.00"))

    def test_sales_item_total_with_vat(self):
        expected_total_with_vat = Decimal("100.00") + (
            Decimal("50.00") * 2 * Decimal("13") / 100
        )
        self.assertEqual(self.sales_item.total_with_vat, int(expected_total_with_vat))


class PaymentTest(TestCase):
    def setUp(self):
        self.tenant = TenantModel.objects.create(
            name="Test Tenant", domain="testdomain"
        )
        self.customer = Customer.objects.create(
            tenant=self.tenant,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="123456789",
            address="123 Main St",
        )
        self.payment = PaymentReceived.objects.create(
            tenant=self.tenant,
            amount=Decimal("50.00"),
            payment_method="Credit Card",
            transaction_id="1234567890",
            customer=self.customer,
        )

    def test_payment_received_str(self):
        self.assertEqual(str(self.payment.amount), f"{Decimal('50.00')}")


class SupplierTest(TestCase):
    def setUp(self):
        self.tenant = TenantModel.objects.create(
            name="Test Tenant", domain="testdomain"
        )
        self.supplier = Supplier.objects.create(
            tenant=self.tenant,
            name="Test Supplier",
            contact_person="Jane Doe",
            email="supplier@example.com",
            phone_number="987654321",
            address="456 Elm St",
        )
        self.purchase_invoice = PurchaseInvoice.objects.create(
            tenant=self.tenant,
            supplier=self.supplier,
            invoice_number="INV123",
            total_amount=Decimal("200.00"),
            received_date=None,
            order_date=None,
        )

    def test_supplier_get_remaining_balance(self):
        remaining_balance = self.supplier.get_remaining_balance(self.tenant)
        expected_balance = Decimal("200.00") - Decimal("0.00")  # No payments made yet
        self.assertEqual(remaining_balance, expected_balance)


class PurchaseInvoiceTest(TestCase):
    def setUp(self):
        self.tenant = TenantModel.objects.create(
            name="Test Tenant", domain="testdomain"
        )
        self.supplier = Supplier.objects.create(
            tenant=self.tenant,
            name="Test Supplier",
            contact_person="Jane Doe",
            email="supplier@example.com",
            phone_number="987654321",
            address="456 Elm St",
        )
        self.purchase_invoice = PurchaseInvoice.objects.create(
            tenant=self.tenant,
            supplier=self.supplier,
            invoice_number="INV123",
            total_amount=Decimal("200.00"),
            received_date=None,
            order_date=None,
        )

    def test_purchase_invoice_str(self):
        self.assertEqual(
            str(self.purchase_invoice),
            f"Purchase #{self.purchase_invoice.id} - {self.supplier.name}",
        )

    def test_purchase_invoice_calculate_lead_time(self):
        self.purchase_invoice.order_date = (
            self.purchase_invoice.purchase_date - timedelta(days=5)
        )
        self.purchase_invoice.save()
        lead_time = self.purchase_invoice.calculate_lead_time()
        self.assertEqual(lead_time, timedelta(days=5))


class PurchaseItemTest(TestCase):
    def setUp(self):
        self.tenant = TenantModel.objects.create(
            name="Test Tenant", domain="testdomain"
        )
        self.product = Product.objects.create(
            tenant=self.tenant,
            name="Test Product",
            uom=UnitOfMeasurements.objects.create(name="Unit", field="FLOAT"),
            sku="TEST123",
            stock_quantity=100.0,
            opening_stock=50,
        )
        self.purchase_invoice = PurchaseInvoice.objects.create(
            tenant=self.tenant,
            supplier=Supplier.objects.create(
                tenant=self.tenant,
                name="Test Supplier",
                contact_person="Jane Doe",
                email="supplier@example.com",
                phone_number="987654321",
                address="456 Elm St",
            ),
            invoice_number="INV123",
            total_amount=Decimal("200.00"),
            received_date=None,
            order_date=None,
        )
        self.purchase_item = PurchaseItem.objects.create(
            tenant=self.tenant,
            purchase=self.purchase_invoice,
            product=self.product,
            quantity=5,
            price=Decimal("40.00"),
        )

    def test_purchase_item_total(self):
        self.assertEqual(self.purchase_item.total, Decimal("200.00"))


class StockMovementTest(TestCase):
    def setUp(self):
        self.tenant = TenantModel.objects.create(
            name="Test Tenant", domain="testdomain"
        )
        self.product = Product.objects.create(
            tenant=self.tenant,
            name="Test Product",
            uom=UnitOfMeasurements.objects.create(name="Unit", field="FLOAT"),
            sku="TEST123",
            stock_quantity=100.0,
            opening_stock=50,
        )

    def test_stock_movement_creation(self):
        StockMovement.objects.create(
            tenant=self.tenant,
            product=self.product,
            movement_type="OUT PURCHASE RETURN",
            quantity=2,
            description="Test stock movement",
        )
        stock_movement = StockMovement.objects.get(
            product=self.product, movement_type="OUT PURCHASE RETURN"
        )
        self.assertEqual(stock_movement.quantity, 2)


class PurchaseReturnTest(TestCase):
    def setUp(self):
        self.tenant = TenantModel.objects.create(
            name="Test Tenant", domain="testdomain"
        )
        self.product = Product.objects.create(
            tenant=self.tenant,
            name="Test Product",
            uom=UnitOfMeasurements.objects.create(name="Unit", field="FLOAT"),
            sku="TEST123",
            stock_quantity=100.0,
            opening_stock=50,
        )
        self.purchase_invoice = PurchaseInvoice.objects.create(
            tenant=self.tenant,
            supplier=Supplier.objects.create(
                tenant=self.tenant,
                name="Test Supplier",
                contact_person="Jane Doe",
                email="supplier@example.com",
                phone_number="987654321",
                address="456 Elm St",
            ),
            invoice_number="INV123",
            total_amount=Decimal("200.00"),
            received_date=None,
            order_date=None,
        )
        self.purchase_return = PurchaseReturn.objects.create(
            tenant=self.tenant,
            purchase_invoice=self.purchase_invoice,
            total_amount=Decimal("100.00"),
        )
        self.purchase_return_item = PurchaseReturnItem.objects.create(
            tenant=self.tenant,
            purchase_return=self.purchase_return,
            product=self.product,
            quantity=2,
            price=Decimal("40.00"),
        )

    def test_purchase_return_str(self):
        self.assertEqual(
            str(self.purchase_return),
            f"Purchase Return #{self.purchase_return.id} for Invoice #{self.purchase_invoice.id}",
        )

    def test_purchase_return_item_total(self):
        self.assertEqual(self.purchase_return_item.total, Decimal("80.00"))

    def test_handle_purchase_return_stock_movement(self):
        # Trigger post_save signal manually
        StockMovement.objects.create(
            tenant=self.tenant,
            product=self.purchase_return_item.product,
            movement_type="OUT PURCHASE RETURN",
            quantity=self.purchase_return_item.quantity,
            description=f"Purchase Return #{self.purchase_return.id}",
        )
        self.product.refresh_from_db()
        self.assertEqual(
            self.product.stock_quantity, 100.0 - self.purchase_return_item.quantity
        )
