from rest_framework import viewsets
from accountType.models import AccountType
from accountType.account_type_serializers import AccountTypeSerializer


class AccountTypeViewSet(viewsets.ModelViewSet):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer
