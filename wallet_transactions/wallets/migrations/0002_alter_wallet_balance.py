# Generated by Django 4.2 on 2023-04-03 11:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wallets", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wallet",
            name="balance",
            field=models.FloatField(null=True),
        ),
    ]
