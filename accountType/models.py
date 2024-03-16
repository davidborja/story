from django.db import models

# Create your models here.


class AccountType(models.Model):
    TYPE_CHOICES = [
        ("credit", "Credit"),
        ("debit", "Debit"),
    ]
    type = models.CharField(max_length=6, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.type}"
