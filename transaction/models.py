from django.db import models

# Create your models here.


class Transaction(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    movement_date = models.DateField()

    def __str__(self):
        return f"{self.id} {self.amount}"
