from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
import random
import string


from .list_for_model import TYPEOFWALLET, CURRENCYS

User = settings.AUTH_USER_MODEL
COUNT_OF_WALLET_YOU_CAN_CREAT = 5
FOR_NEW_WALLET_RUB_100 = 100
FOR_NEW_WALLET_USD_EUR_3 = 3
CHECK = True


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


@receiver(post_save, sender=Wallet)
def add_balance_wallet(sender, instance, created, *args, **kwargs):
    """Add balance for wallet when wallet create"""
    if created:
        if instance.currency == "RUB":
            instance.balance = FOR_NEW_WALLET_RUB_100
        else:
            instance.balance = FOR_NEW_WALLET_USD_EUR_3

        instance.save()


@receiver(post_save, sender=Wallet)
def add_name_wallet(sender, instance, created, *args, **kwargs):
    """Add name for wallet when wallet create"""
    if created:
        global CHECK, name
        if not instance.name:
            while CHECK:
                name = [
                    random.choice(string.ascii_uppercase + string.digits)
                    for i in range(8)
                ]
                check_name = Wallet.objects.filter(name=name).count()
                if check_name == 0:
                    CHECK = False
            instance.name = "".join(name)

        instance.save()
