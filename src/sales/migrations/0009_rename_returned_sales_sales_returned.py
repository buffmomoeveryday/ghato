# Generated by Django 5.0.6 on 2024-09-12 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0008_sales_returned_sales'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sales',
            old_name='Returned sales',
            new_name='returned',
        ),
    ]
