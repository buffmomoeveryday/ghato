# Generated by Django 5.0.6 on 2024-07-22 03:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("sales", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="salesinvoice",
            old_name="order",
            new_name="sales",
        ),
    ]
