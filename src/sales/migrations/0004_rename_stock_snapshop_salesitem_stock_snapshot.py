# Generated by Django 5.0.6 on 2024-07-30 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_salesitem_stock_snapshop'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salesitem',
            old_name='stock_snapshop',
            new_name='stock_snapshot',
        ),
    ]
