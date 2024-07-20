from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['label', 'balance']
    ordering_fields = ['label', 'balance', 'id']
    ordering = ['-balance']


class TransactionViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['amount', 'wallet', ]
    ordering_fields = ['txid', 'amount', 'id', ]
    ordering = ['-id']
