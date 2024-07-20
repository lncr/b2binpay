from django.db import models
from django.core.validators import MinValueValidator


class Wallet(models.Model):
    label = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=50, decimal_places=18, default=0.0, validators=[MinValueValidator(0.0)])

    def __str__(self):
        return f'Wallet {self.label}'


class Transaction(models.Model):
    txid = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=50, decimal_places=18)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return f'Transaction {self.txid}'
