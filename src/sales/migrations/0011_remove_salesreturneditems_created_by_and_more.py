# Generated by Django 5.1.1 on 2024-09-23 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0010_alter_salesinvoice_sales_salesreturn_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesreturneditems',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='salesreturneditems',
            name='tenant',
        ),
        migrations.DeleteModel(
            name='SalesReturn',
        ),
        migrations.DeleteModel(
            name='SalesReturnedItems',
        ),
    ]
