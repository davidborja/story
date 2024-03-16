from rest_framework import viewsets
from transaction.models import Transaction
from transaction.transaction_serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
