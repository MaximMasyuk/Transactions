# Generated by Django 4.2 on 2023-04-05 06:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wallets", "0012_remove_wallet_count"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wallet",
            name="balance",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
    ]
