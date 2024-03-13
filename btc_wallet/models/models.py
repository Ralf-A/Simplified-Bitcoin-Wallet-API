from django.db import models
import uuid


class Transaction(models.Model):
    # A random unique hexadecimal string
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Amount in BTC, with max_digits set to accommodate the largest possible BTC value and decimal_places for precision
    amount = models.DecimalField(max_digits=19, decimal_places=10)
    # Whether this transaction has been used in a money transfer
    spent = models.BooleanField(default=False)
    # The timestamp when this transaction was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_id}"
