# Generated by Django 4.2 on 2023-04-05 07:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wallets", "0015_alter_wallet_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wallet",
            name="name",
            field=models.CharField(blank=True, null=True),
        ),
    ]
