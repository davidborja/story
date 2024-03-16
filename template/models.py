from django.db import models

# Create your models here.


class Template(models.Model):
    TYPE_CHOICES = [("email", "Email")]
    type = models.CharField(max_length=6, choices=TYPE_CHOICES)
    html = models.CharField(max_length=8000000)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id} {self.type}"
