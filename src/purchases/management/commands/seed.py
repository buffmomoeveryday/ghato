import random
from django.core.management.base import BaseCommand
from faker import Faker
from tenant.models import TenantModel
from purchases.models import (
    UnitOfMeasurements,
    Product,
    StockMovement,
    PaymentMade,
    Supplier,
    PurchaseInovice,
    PurchaseItem,
)


class Command(BaseCommand):
    help = "Seed the database with initial data for a specific tenant."

    def add_arguments(self, parser):
        parser.add_argument(
            "tenant_name", type=str, help="Name of the tenant to seed data for"
        )
        parser.add_argument(
            "--num_uoms",
            type=int,
            default=2,
            help="Number of unit of measurements to create",
        )
        parser.add_argument(
            "--num_suppliers", type=int, default=5, help="Number of suppliers to create"
        )
        parser.add_argument(
            "--num_products", type=int, default=10, help="Number of products to create"
        )
        parser.add_argument(
            "--num_stock_movements",
            type=int,
            default=10,
            help="Number of stock movements to create",
        )
        parser.add_argument(
            "--num_purchase_invoices",
            type=int,
            default=5,
            help="Number of purchase invoices to create",
        )
        parser.add_argument(
            "--num_purchase_items",
            type=int,
            default=5,
            help="Number of purchase items per invoice to create",
        )
        parser.add_argument(
            "--num_payments", type=int, default=5, help="Number of payments to create"
        )

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting database seeding..."))

        tenant_name = kwargs["tenant_name"]
        num_uoms = kwargs["num_uoms"]
        num_suppliers = kwargs["num_suppliers"]
        num_products = kwargs["num_products"]
        num_stock_movements = kwargs["num_stock_movements"]
        num_purchase_invoices = kwargs["num_purchase_invoices"]
        num_purchase_items = kwargs["num_purchase_items"]
        num_payments = kwargs["num_payments"]

        faker = Faker()

        # Fetch the specified tenant
        try:
            tenant = TenantModel.objects.get(name=tenant_name)
        except TenantModel.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"Tenant with name {tenant_name} does not exist.")
            )
            return

        # Create UnitOfMeasurements
        uoms = []
        for _ in range(num_uoms):
            uom = UnitOfMeasurements.objects.create(
                name=faker.word().capitalize(),
                field=random.choice(["1", "2"]),
                tenant=tenant,
            )
            uoms.append(uom)

        # Create Suppliers
        suppliers = []
        for _ in range(num_suppliers):
            supplier = Supplier.objects.create(
                name=faker.company(),
                contact_person=faker.name(),
                email=faker.email(),
                phone_number=faker.phone_number(),
                address=faker.address(),
                tenant=tenant,
            )
            suppliers.append(supplier)

        # Create Products
        products = []
        for _ in range(num_products):
            product = Product.objects.create(
                name=faker.word().capitalize(),
                uom=random.choice(uoms),
                sku=faker.unique.bothify(text="SKU-####"),
                stock_quantity=random.randint(0, 500),
                tenant=tenant,
            )
            products.append(product)

        # Create Stock Movements
        for _ in range(num_stock_movements):
            StockMovement.objects.create(
                product=random.choice(products),
                movement_type=random.choice(["IN", "OUT"]),
                quantity=random.randint(1, 100),
                description=faker.sentence(),
                tenant=tenant,
            )

        # Create Purchase Invoices
        purchase_invoices = []
        for _ in range(num_purchase_invoices):
            supplier = random.choice(suppliers)
            purchase_invoice = PurchaseInovice.objects.create(
                supplier=supplier,
                invoice_number=faker.unique.bothify(text="INV-#####"),
                total_amount=random.uniform(100.00, 5000.00),
                tenant=tenant,
            )
            purchase_invoices.append(purchase_invoice)

        # Create Purchase Items
        for purchase_invoice in purchase_invoices:
            for _ in range(random.randint(1, num_purchase_items)):
                PurchaseItem.objects.create(
                    purchase=purchase_invoice,
                    product=random.choice(products),
                    quantity=random.randint(1, 50),
                    price=random.uniform(10.00, 200.00),
                    tenant=tenant,
                )

        # Create Payments Made
        for _ in range(num_payments):
            supplier = random.choice(suppliers)
            PaymentMade.objects.create(
                amount=random.uniform(50.00, 2000.00),
                payment_method=random.choice(["Credit Card", "Bank Transfer", "Cash"]),
                transaction_id=faker.unique.bothify(text="TRANS-#####"),
                supplier=supplier,
                tenant=tenant,
            )

        self.stdout.write(
            self.style.SUCCESS("Database seeding completed successfully.")
        )
