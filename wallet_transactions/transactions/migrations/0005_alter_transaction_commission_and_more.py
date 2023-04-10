# Generated by Django 4.2 on 2023-04-06 09:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("transactions", "0004_alter_transaction_commission_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="commission",
            field=models.DecimalField(
                blank=True, decimal_places=2, editable=False, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[("PAID", "PAID"), ("FAILED", "FAILED")],
                editable=False,
                max_length=25,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="timestamp",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
