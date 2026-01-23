from django.db import models

# Create your models here.
class Expenses(models.Model):
    expenseName = models.CharField(max_length=100)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    currency = models.CharField(
        max_length=3,
        choices=[('INR', 'INR'), ('USD', 'USD')]
    )
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.subject} - {self.amount} {self.currency}"