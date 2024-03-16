from rest_framework import serializers
from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "amount_limit",
            "account_creation_date",
            "account_type",
            "transaction",
            "user",
        ]
