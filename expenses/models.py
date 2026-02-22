# from django.db import models

# Categories = (('noCategory','No Category'),('food','Food'))

# # Create your models here.
# class Expense(models.Model):
#     expenseName = models.CharField(max_length=100)
#     category = models.CharField(max_length=10,choices=Categories,default='noCategory')
#     date = models.DateField()
#     amount = models.DecimalField(max_digits=10,decimal_places=2)
#     currency = models.CharField(
#         max_length=3,
#         choices=[('INR', 'INR'), ('USD', 'USD')]
#     )
#     description = models.TextField(blank=True)
    
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.expenseName} - {self.amount} {self.currency}"

from django.db import models
from django.contrib.auth.models import User

Categories = (('noCategory','No Category'),('food','Food'))

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   # ✅ ADD THIS
    expenseName = models.CharField(max_length=100)
    category = models.CharField(max_length=10,choices=Categories,default='noCategory')
    date = models.DateField()
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    currency = models.CharField(
        max_length=3,
        choices=[('INR', 'INR'), ('USD', 'USD')]
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.expenseName} - {self.amount} {self.currency}"