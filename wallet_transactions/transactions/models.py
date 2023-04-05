from django.db import models

from wallets.models import Wallet

# Create your models here.


class Transaction(models.Model):
    sender = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="receiver"
    )
    transfer_amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=25)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (
            f"sender: {self.sender}, recever: {self.receiver},"
            f"transfer amount: {self.transfer_amount}"
        )
