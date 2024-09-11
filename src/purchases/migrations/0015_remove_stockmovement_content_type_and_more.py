# Generated by Django 5.0.6 on 2024-08-21 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0014_stockmovement_content_type_stockmovement_object_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockmovement',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='stockmovement',
            name='object_id',
        ),
        migrations.AlterField(
            model_name='stockmovement',
            name='movement_type',
            field=models.CharField(choices=[('IN', 'Stock In'), ('OUT', 'Stock Out'), ('IN SALES RETURN', 'Stock In Sales Return'), ('OUT PURCHASE RETURN', 'Stock Out Purchase Return')], max_length=20),
        ),
    ]