from celery import shared_task

from purchases.models import Product, PurchaseItem


@shared_task
def add_to_stock(product_id, purchase_item_id):
    product = Product.objects.filter(id=product_id)
    purchase_item = PurchaseItem.objects.filter(Id=purchase_item_id)

