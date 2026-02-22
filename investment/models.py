# from django.db import models

# # Create your models here.
# class Investment(models.Model):
#     investmentName = models.CharField(max_length=100)
#     date = models.DateField()
#     amount = models.DecimalField(max_digits=10,decimal_places=2)
#     currency = models.CharField(
#         max_length=3,
#         choices=[('INR', 'INR'), ('USD', 'USD')]
#     )
#     description = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.investmentName} - {self.amount} {self.currency}"

from django.db import models
from django.contrib.auth.models import User

class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   # ✅ ADD THIS
    investmentName = models.CharField(max_length=100)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    currency = models.CharField(
        max_length=3,
        choices=[('INR', 'INR'), ('USD', 'USD')]
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.investmentName} - {self.amount} {self.currency}"