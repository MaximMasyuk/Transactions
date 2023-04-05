from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.conf import settings


from .list_for_model import TYPEOFWALLET, CURRENCYS

User = settings.AUTH_USER_MODEL
COUNTOFWALLETYOUCANCREAT = 5
FORNEWWALLETRUB100 = 100
FORNEWWALLETUSDEUR3 = 3


class Wallet(models.Model):
    """Describe table Wallet"""

    name = models.CharField(blank=True, null=True, editable=False, unique=True)
    type_of_wallet = models.CharField(choices=TYPEOFWALLET, max_length=15)
    currency = models.CharField(choices=CURRENCYS, max_length=4)
    balance = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=2, editable=False
    )
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"


@receiver(pre_save, sender=Wallet)
def add_balance_wallet(sender, instance, *args, **kwargs):
    """Pre-save method when wallet is created check the currency
    and add the balance for new user"""
    if not instance.balance:
        if instance.currency == "RUB":
            instance.balance = FORNEWWALLETRUB100
        else:
            instance.balance = FORNEWWALLETUSDEUR3
