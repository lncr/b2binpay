from django.db import transaction
from rest_framework import serializers

from wallets.models import Transaction, Wallet


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ['id', 'label', 'balance', ]
        read_only_fields = ['balance', ]


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['id', 'wallet_id', 'txid', 'amount', ]

    def validate(self, data: dict) -> dict:
        wallet = data['wallet']
        amount = data['amount']
        if wallet.balance + amount < 0:
            raise serializers.ValidationError("Transaction is impossible. Insufficient balance")
        return data

    def create(self, validated_data: dict) -> Transaction:
        wallet = validated_data['wallet']
        amount = validated_data['amount']

        with transaction.atomic():
            wallet.balance += amount
            wallet.save()
            wallet_transaction = Transaction.objects.create(**validated_data)

        return wallet_transaction
