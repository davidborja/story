from django.db import models
from accountType.models import AccountType
from user.models import User
from transaction.models import Transaction

# Create your models here.


class Account(models.Model):
    amount_limit = models.DecimalField(max_digits=10, decimal_places=2)
    account_creation_date = models.DateField()
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    transaction = models.ManyToManyField(Transaction, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
