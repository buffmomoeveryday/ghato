# Generated by Django 5.0.6 on 2024-08-19 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0012_rename_purchaseinovice_purchaseinvoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitofmeasurements',
            name='field',
            field=models.CharField(blank=True, choices=[('FLOAT', 'Float'), ('INTEGER', 'Integer')], default='FLOAT', max_length=255, null=True),
        ),
    ]