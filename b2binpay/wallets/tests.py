from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from wallets.models import Wallet, Transaction


class WalletsTesCase(APITestCase):

    def setUp(self) -> None:
        self.empty_wallet = Wallet.objects.create(label='test_wallet')
        self.wallet_with_funds = Wallet.objects.create(label='test_wallet1')
        self.positive_transaction = Transaction.objects.create(txid='uniquetxid', wallet_id=self.wallet_with_funds.id,
                                                               amount=12.345)
        self.negative_transaction = Transaction.objects.create(txid='uniquetxid1', wallet_id=self.wallet_with_funds.id,
                                                               amount=-6.789)

    def test_wallet_list(self):
        url = reverse('wallet-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)

    def test_wallet_detail(self):
        url = reverse('wallet-detail', kwargs={'pk': self.wallet_with_funds.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wallet_create(self):
        url = reverse('wallet-list')
        data = {'label': 'new label', }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_transactions_list(self):
        url = reverse('transaction-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_transaction_detail(self):
        url = reverse('transaction-detail', kwargs={'pk': self.positive_transaction.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.positive_transaction.id)

    def test_create_positive_transaction(self):
        url = reverse('transaction-list')
        amount = 12.33
        data = {'txid': 'test_create_positive_trans', 'amount': amount, 'wallet': self.wallet_with_funds.id}
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_impossible_negative_transaction(self):
        url = reverse('transaction-list')
        data = {'txid': 'test_create_positive_trans', 'amount': -12.33, 'wallet': self.empty_wallet.id}
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

