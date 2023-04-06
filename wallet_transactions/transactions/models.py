from django.db import models

from wallets.models import Wallet


PAID = "PAID"
FAILED = "FAILED"

STATUS_TYPE = [
    (PAID, "PAID"),
    (FAILED, "FAILED"),
]


class Transaction(models.Model):
    """Describe table Transaction"""

    sender = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="receiver"
    )
    transfer_amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False, null=True, blank=True
    )
    status = models.CharField(
        choices=STATUS_TYPE, max_length=25, editable=False, null=True, blank=True
    )
    timestamp = models.DateTimeField(
        auto_now_add=True, editable=False, null=True, blank=True
    )

    def __str__(self) -> str:
        """Returns String representation for Transaction"""
        return (
            f"sender: {self.sender}, recever: {self.receiver},"
            f"transfer amount: {self.transfer_amount}"
        )
