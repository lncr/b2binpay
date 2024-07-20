from django.urls import path, include
from rest_framework import routers

from wallets.views import WalletViewSet, TransactionViewSet

router = routers.DefaultRouter()

router.register(r'wallets', WalletViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
