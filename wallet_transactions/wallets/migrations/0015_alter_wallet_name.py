# Generated by Django 4.2 on 2023-04-05 06:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wallets", "0014_alter_wallet_balance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wallet",
            name="name",
            field=models.CharField(blank=True, editable=False, null=True),
        ),
    ]