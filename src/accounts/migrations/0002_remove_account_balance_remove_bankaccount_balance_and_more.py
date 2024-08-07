# Generated by Django 5.0.6 on 2024-07-17 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="account",
            name="balance",
        ),
        migrations.RemoveField(
            model_name="bankaccount",
            name="balance",
        ),
        migrations.RemoveField(
            model_name="cashaccount",
            name="balance",
        ),
        migrations.AddField(
            model_name="bankaccount",
            name="type",
            field=models.CharField(
                choices=[("1", "CURRENT"), ("2", "SAVING")], default="1", max_length=25
            ),
        ),
        migrations.AddField(
            model_name="cashaccount",
            name="name",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
