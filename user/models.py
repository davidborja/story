from django.db import models

# Create your models here.


# Extending User Model
class User(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    email = models.CharField(max_length=18, unique=True)
    curp = models.CharField(max_length=18, unique=True)
    rfc = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return f"{self.name} {self.last_name}"
