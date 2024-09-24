from django.test import TestCase
from purchases.models import (
    UnitOfMeasurements,
    Product,
    StockMovement,
    PaymentMade,
    Supplier,
    PurchaseInvoice,
    PurchaseItem,
    PurchaseReturn,
    PurchaseReturnItem,
)
from tenant.models import TenantModel

from django.utils import timezone
from decimal import Decimal


class UnitOfMeasurementsTestCase(TestCase):
    def setUp(self):
        self.tenant = TenantModel.objects.create(name="Tenant UOM", domain="tenantuom")
        self.uom = UnitOfMeasurements.objects.create(
            name="Kilogram",
            field=UnitOfMeasurements.FieldType.FLOAT,
            tenant=self.tenant,
        )

    def test_uom_creation(self):
        self.assertEqual(self.uom.name, "Kilogram")
        self.assertEqual(self.uom.field, "FLOAT")
        self.assertEqual(self.uom.tenant, self.tenant)

    def test_uom_update(self):
        self.uom.name = "Gram"
        self.uom.save()
        self.uom.refresh_from_db()
        self.assertEqual(self.uom.name, "Gram")

    def test_uom_delete(self):
        uom_id = self.uom.id
        self.uom.delete()
        with self.assertRaises(UnitOfMeasurements.DoesNotExist):
            UnitOfMeasurements.objects.get(id=uom_id)


class ProductTestCase(TestCase):
    def setUp(self):
        self.tenant = TenantModel.objects.create(
            name="Tenant Product", domain="tenantproduct"
        )
        self.uom = UnitOfMeasurements.objects.create(
            name="Piece", field=UnitOfMeasurements.FieldType.INT, tenant=self.tenant
        )
        self.product = Product.objects.create(
            name="Widget",
            uom=self.uom,
            sku="WIDGET123",
            stock_quantity=100.0,
            opening_stock=50,
            tenant=self.tenant,
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Widget")
        self.assertEqual(self.product.uom, self.uom)
        self.assertEqual(self.product.sku, "WIDGET123")
        self.assertEqual(self.product.tenant, self.tenant)

    def test_product_update(self):
        self.product.name = "Gizmo"
        self.product.save()
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Gizmo")

    def test_product_delete(self):
        product_id = self.product.id
        self.product.delete()
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=product_id)


class StockMovementTestCase(TestCase):
    def setUp(self):
        self.tenant = TenantModel.objects.create(
            name="Tenant Stock", domain="tenantstock"
        )
        self.uom = UnitOfMeasurements.objects.create(
            name="Box", field=UnitOfMeasurements.FieldType.FLOAT, tenant=self.tenant
        )
        self.product = Product.objects.create(
            name="Gadget",
            uom=self.uom,
            sku="GADGET123",
            stock_quantity=200.0,
            opening_stock=150,
            tenant=self.tenant,
        )
        self.stock_movement = StockMovement.objects.create(
            product=self.product, movement_type="IN", quantity=50, tenant=self.tenant
        )

    def test_stock_movement_creation(self):
        self.assertEqual(self.stock_movement.product, self.product)
        self.assertEqual(self.stock_movement.movement_type, "IN")
        self.assertEqual(self.stock_movement.quantity, 50)
        self.assertEqual(self.stock_movement.tenant, self.tenant)

    def test_stock_movement_update(self):
        self.stock_movement.quantity = 100
        self.stock_movement.save()
        self.stock_movement.refresh_from_db()
        self.assertEqual(self.stock_movement.quantity, 100)

    def test_stock_movement_delete(self):
        stock_movement_id = self.stock_movement.id
        self.stock_movement.delete()
        with self.assertRaises(StockMovement.DoesNotExist):
            StockMovement.objects.get(id=stock_movement_id)


class PaymentMadeTestCase(TestCase):
    def setUp(self):
        self.tenant = TenantModel.objects.create(
            name="Tenant Payment", domain="tenantpayment"
        )
        self.supplier = Supplier.objects.create(name="ABC Supplies", tenant=self.tenant)
        self.payment = PaymentMade.objects.create(
            amount=Decimal("100.00"),
            payment_method="Credit Card",
            transaction_id="TRANS123",
            supplier=self.supplier,
            tenant=self.tenant,
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.amount, Decimal("100.00"))
        self.assertEqual(self.payment.payment_method, "Credit Card")
        self.assertEqual(self.payment.transaction_id, "TRANS123")
        self.assertEqual(self.payment.supplier, self.supplier)
        self.assertEqual(self.payment.tenant, self.tenant)

    def test_payment_update(self):
        self.payment.amount = Decimal("150.00")
        self.payment.save()
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.amount, Decimal("150.00"))

    def test_payment_delete(self):
        payment_id = self.payment.id
        self.payment.delete()
        with self.assertRaises(PaymentMade.DoesNotExist):
            PaymentMade.objects.get(id=payment_id)


class SupplierTestCase(TestCase):
    def setUp(self):
        self.tenant = TenantModel.objects.create(
            name="Tenant Supplier", domain="tenantsupplier"
        )
        self.supplier = Supplier.objects.create(name="XYZ Supplies", tenant=self.tenant)

    def test_supplier_creation(self):
        self.assertEqual(self.supplier.name, "XYZ Supplies")
        self.assertEqual(self.supplier.tenant, self.tenant)

    def test_supplier_update(self):
        self.supplier.name = "Updated Supplies"
        self.supplier.save()
        self.supplier.refresh_from_db()
        self.assertEqual(self.supplier.name, "Updated Supplies")

    def test_supplier_delete(self):
        supplier_id = self.supplier.id
        self.supplier.delete()
        with self.assertRaises(Supplier.DoesNotExist):
            Supplier.objects.get(id=supplier_id)


class PurchaseInvoiceTestCase(TestCase):
    def setUp(self):
        self.tenant = TenantModel.objects.create(
            name="Tenant Invoice", domain="tenantinvoice"
        )
        self.supplier = Supplier.objects.create(name="LMN Supplies", tenant=self.tenant)
        self.purchase_invoice = PurchaseInvoice.objects.create(
            supplier=self.supplier, total_amount=Decimal("500.00"), tenant=self.tenant
        )

    def test_purchase_invoice_creation(self):
        self.assertEqual(self.purchase_invoice.supplier, self.supplier)
        self.assertEqual(self.purchase_invoice.total_amount, Decimal("500.00"))
        self.assertEqual(self.purchase_invoice.tenant, self.tenant)

    def test_purchase_invoice_update(self):
        self.purchase_invoice.total_amount = Decimal("600.00")
        self.purchase_invoice.save()
        self.purchase_invoice.refresh_from_db()
        self.assertEqual(self.purchase_invoice.total_amount, Decimal("600.00"))

    def test_purchase_invoice_delete(self):
        purchase_invoice_id = self.purchase_invoice.id
        self.purchase_invoice.delete()
        with self.assertRaises(PurchaseInvoice.DoesNotExist):
            PurchaseInvoice.objects.get(id=purchase_invoice_id)


class PurchaseItemTestCase(TestCase):
    def setUp(self):
        self.tenant = TenantModel.objects.create(
            name="Tenant Item", domain="tenantitem"
        )
        self.supplier = Supplier.objects.create(name="DEF Supplies", tenant=self.tenant)
        self.uom = UnitOfMeasurements.objects.create(
            name="Set", field=UnitOfMeasurements.FieldType.FLOAT, tenant=self.tenant
        )
        self.product = Product.objects.create(
            name="Thingamajig",
            uom=self.uom,
            sku="THING123",
            stock_quantity=300.0,
            opening_stock=250,
            tenant=self.tenant,
        )
        self.purchase_invoice = PurchaseInvoice.objects.create(
            supplier=self.supplier, total_amount=Decimal("750.00"), tenant=self.tenant
        )
        self.purchase_item = PurchaseItem.objects.create(
            purchase=self.purchase_invoice,
            product=self.product,
            quantity=10,
            price=Decimal("75.00"),
            tenant=self.tenant,
        )

    def test_purchase_item_creation(self):
        self.assertEqual(self.purchase_item.purchase, self.purchase_invoice)
        self.assertEqual(self.purchase_item.product, self.product)
        self.assertEqual(self.purchase_item.quantity, 10)
        self.assertEqual(self.purchase_item.price, Decimal("75.00"))
        self.assertEqual(self.purchase_item.tenant, self.tenant)

    def test_purchase_item_update(self):
        self.purchase_item.quantity = 20
        self.purchase_item.save()
        self.purchase_item.refresh_from_db()
        self.assertEqual(self.purchase_item.quantity, 20)

    def test_purchase_item_delete(self):
        purchase_item_id = self.purchase_item.id
        self.purchase_item.delete()
        with self.assertRaises(PurchaseItem.DoesNotExist):
            PurchaseItem.objects.get(id=purchase_item_id)


class PurchaseReturnTestCase(TestCase):
    def setUp(self):
        self.tenant = TenantModel.objects.create(
            name="Tenant Return", domain="tenantreturn"
        )
        self.supplier = Supplier.objects.create(name="HIJ Supplies", tenant=self.tenant)
        self.purchase_invoice = PurchaseInvoice.objects.create(
            supplier=self.supplier, total_amount=Decimal("300.00"), tenant=self.tenant
        )
        self.purchase_return = PurchaseReturn.objects.create(
            purchase_invoice=self.purchase_invoice,
            total_amount=Decimal("100.00"),
            tenant=self.tenant,
        )

    def test_purchase_return_creation(self):
        self.assertEqual(self.purchase_return.purchase_invoice, self.purchase_invoice)
        self.assertEqual(self.purchase_return.total_amount, Decimal("100.00"))
        self.assertEqual(self.purchase_return.tenant, self.tenant)

    def test_purchase_return_update(self):
        self.purchase_return.total_amount = Decimal("150.00")
        self.purchase_return.save()
        self.purchase_return.refresh_from_db()
        self.assertEqual(self.purchase_return.total_amount, Decimal("150.00"))

    def test_purchase_return_delete(self):
        purchase_return_id = self.purchase_return.id
        self.purchase_return.delete()
        with self.assertRaises(PurchaseReturn.DoesNotExist):
            PurchaseReturn.objects.get(id=purchase_return_id)


class PurchaseReturnItemTestCase(TestCase):
    def setUp(self):
        self.tenant = TenantModel.objects.create(
            name="Tenant Return Item", domain="tenantreturnitem"
        )
        self.supplier = Supplier.objects.create(name="GHI Supplies", tenant=self.tenant)
        self.uom = UnitOfMeasurements.objects.create(
            name="Pack", field=UnitOfMeasurements.FieldType.FLOAT, tenant=self.tenant
        )
        self.product = Product.objects.create(
            name="Doohickey",
            uom=self.uom,
            sku="DOOH123",
            stock_quantity=400.0,
            opening_stock=350,
            tenant=self.tenant,
        )
        self.purchase_invoice = PurchaseInvoice.objects.create(
            supplier=self.supplier, total_amount=Decimal("900.00"), tenant=self.tenant
        )
        self.purchase_return = PurchaseReturn.objects.create(
            purchase_invoice=self.purchase_invoice,
            total_amount=Decimal("200.00"),
            tenant=self.tenant,
        )
        self.purchase_return_item = PurchaseReturnItem.objects.create(
            purchase_return=self.purchase_return,
            product=self.product,
            quantity=5,
            price=Decimal("40.00"),
            tenant=self.tenant,
        )

    def test_purchase_return_item_creation(self):
        self.assertEqual(
            self.purchase_return_item.purchase_return, self.purchase_return
        )
        self.assertEqual(self.purchase_return_item.product, self.product)
        self.assertEqual(self.purchase_return_item.quantity, 5)
        self.assertEqual(self.purchase_return_item.price, Decimal("40.00"))
        self.assertEqual(self.purchase_return_item.tenant, self.tenant)

    def test_purchase_return_item_update(self):
        self.purchase_return_item.quantity = 10
        self.purchase_return_item.save()
        self.purchase_return_item.refresh_from_db()
        self.assertEqual(self.purchase_return_item.quantity, 10)

    def test_purchase_return_item_delete(self):
        purchase_return_item_id = self.purchase_return_item.id
        self.purchase_return_item.delete()
        with self.assertRaises(PurchaseReturnItem.DoesNotExist):
            PurchaseReturnItem.objects.get(id=purchase_return_item_id)


# views
from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser

class PurchaseIndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.tenant = TenantModel.objects.create(
            name="Test Tenant", domain="testdomain"
        )
        self.user = CustomUser.objects.create_user(
            email="testuser@test.com", password="testpass", tenant=self.tenant
        )
        self.supplier = Supplier.objects.create(
            name="Test Supplier", tenant=self.tenant
        )
        self.purchase_invoice = PurchaseInvoice.objects.create(
            supplier=self.supplier, tenant=self.tenant, total_amount=100
        )
        self.client.login(email="testuser@test.com", password="testpass")

    def test_purchase_index_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("purchase_index"))
        self.assertRedirects(response, "/login/?next=/purchase_index/")

    def test_purchase_index_renders_correct_template(self):
        response = self.client.get(reverse("purchase_index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "purchase/purchase_index.html")

    def test_purchase_index_context_data(self):
        response = self.client.get(reverse("purchase_index"))
        self.assertIn("filter", response.context)
        self.assertEqual(len(response.context["filter"].qs), 1)


class PurchaseAddViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.tenant = TenantModel.objects.create(
            name="Test Tenant", domain="testdomain"
        )
        self.user = CustomUser.objects.create_user(
            email="testuser@test.com", password="testpass", tenant=self.tenant
        )
        self.client.login(email="testuser@test.com", password="testpass")

    def test_purchase_add_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("purchase_add"))
        self.assertRedirects(response, "/login/?next=/purchase_add/")

    def test_purchase_add_renders_correct_template(self):
        response = self.client.get(reverse("purchase_add"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "purchase/purchase_add.html")

    def test_purchase_add_context_data(self):
        response = self.client.get(reverse("purchase_add"))
        self.assertIn("context", response.context)
        self.assertEqual(response.context, {})

from .models import PurchaseItem, Product, UnitOfMeasurements


class PurchaseDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.tenant = TenantModel.objects.create(
            name="Test Tenant", domain="testdomain"
        )
        self.user = CustomUser.objects.create_user(
            email="testuser@test.com", password="testpass", tenant=self.tenant
        )
        self.supplier = Supplier.objects.create(
            name="Test Supplier", tenant=self.tenant
        )
        self.purchase_invoice = PurchaseInvoice.objects.create(
            supplier=self.supplier, tenant=self.tenant, total_amount=100
        )
        self.uom = UnitOfMeasurements.objects.create(
            name="kg", field="FLOAT", tenant=self.tenant
        )
        self.product = Product.objects.create(
            name="Test Product",
            uom=self.uom,
            sku="TESTSKU",
            stock_quantity=10,
            opening_stock=5,
            tenant=self.tenant,
        )
        self.purchase_item = PurchaseItem.objects.create(
            purchase=self.purchase_invoice,
            product=self.product,
            quantity=5,
            price=10,
            tenant=self.tenant,
        )
        self.client.login(email="testuser@test.com", password="testpass")

    def test_purchase_detail_requires_login(self):
        self.client.logout()
        response = self.client.get(
            reverse("purchase_detail", args=[self.purchase_invoice.id])
        )
        self.assertRedirects(
            response, f"/login/?next=/purchase_detail/{self.purchase_invoice.id}/"
        )

    def test_purchase_detail_renders_correct_template(self):
        response = self.client.get(
            reverse("purchase_detail", args=[self.purchase_invoice.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "purchase/purchase_detail.html")

    def test_purchase_detail_context_data(self):
        response = self.client.get(
            reverse("purchase_detail", args=[self.purchase_invoice.id])
        )
        self.assertIn("purchase", response.context)
        self.assertIn("purchase_items", response.context)
        self.assertEqual(response.context["purchase"], self.purchase_invoice)
        self.assertEqual(len(response.context["purchase_items"]), 1)
