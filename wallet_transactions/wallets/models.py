from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.conf import settings

import random
import string

from .list_for_model import TYPEOFWALLET, CURRENCYS

User = settings.AUTH_USER_MODEL


# Create your models here.


class Wallet(models.Model):
    name = models.CharField(blank=True, null=True)
    type_of_wallet = models.CharField(choices=TYPEOFWALLET, max_length=15)
    currency = models.CharField(choices=CURRENCYS, max_length=4)
    balance = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=2
    )
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"


@receiver(pre_save, sender=Wallet)
def add_balance_wallet(sender, instance, *args, **kwargs):
    if not instance.balance:
        if instance.currency == "RUB":
            instance.balance = 100.0
        else:
            instance.balance = 3.0


@receiver(pre_save, sender=Wallet)
def add_name_wallet(sender, instance, *args, **kwargs):
    if not instance.name:
        name = [random.choice(string.ascii_uppercase + string.digits) for i in range(8)]
        instance.name = "".join(name)
