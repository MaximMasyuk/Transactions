from django.db import models

from wallets.models import Wallet

# Create your models here.


class Transaction(models.Model):
    sender = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    transfer_amount = models.FloatField()
    commission = models.FloatField()
    status = models.CharField(max_length=25)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.commission = round(self.commission, 2)
        super(Transaction, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return (
            f"sender: {self.sender}, recever: {self.receiver},"
            f"transfer amount: {self.transfer_amount}"
        )
