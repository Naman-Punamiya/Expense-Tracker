from django.db import models
from django.contrib.auth.models import User

Categories = (('noCategory','No Category'),('food','Food'))


class Account(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class Expense(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    expenseName = models.CharField(max_length=100)
    category = models.CharField(
        max_length=10,
        choices=Categories,
        default='noCategory'
    )
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    currency = models.CharField(
        max_length=3,
        choices=[('INR', 'INR'), ('USD', 'USD')]
    )

    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.name} - {self.expenseName} - {self.amount} {self.currency}"