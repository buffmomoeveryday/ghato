# Generated by Django 5.0.6 on 2024-07-17 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("purchases", "0004_unitofmeasurements_field"),
    ]

    operations = [
        migrations.AlterField(
            model_name="unitofmeasurements",
            name="field",
            field=models.CharField(
                blank=True,
                choices=[("1", ""), ("2", "SAVING")],
                default="1",
                max_length=255,
                null=True,
            ),
        ),
    ]
