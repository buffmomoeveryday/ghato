# Generated by Django 5.0.6 on 2024-07-31 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0008_alter_product_opening_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock_quantity',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='unitofmeasurements',
            name='field',
            field=models.CharField(blank=True, choices=[('1', 'Float'), ('2', 'Integer')], default='1', max_length=255, null=True),
        ),
    ]