# Generated by Django 4.2 on 2023-04-03 12:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("wallets", "0006_alter_wallet_currency"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Currency",
        ),
        migrations.DeleteModel(
            name="TypeOfWalet",
        ),
    ]
