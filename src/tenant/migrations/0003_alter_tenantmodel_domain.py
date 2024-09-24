# Generated by Django 5.1.1 on 2024-09-23 02:36

import tenant.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0002_tenantmodel_api_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenantmodel',
            name='domain',
            field=models.CharField(max_length=10, unique=True, validators=[tenant.models.validate_domain_name], verbose_name='Domain'),
        ),
    ]