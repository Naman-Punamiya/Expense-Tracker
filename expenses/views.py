from django.shortcuts import render,redirect
from .models import Expenses

def add_expenses(request):
    if request.method == "POST":
        Expenses.objects.create(
            expenseName = request.POST['name'],
            date = request.POST['date'],
            amount = request.POST['amount'],
            currency = request.POST['currency'],
            description = request.POST['description'],
        )
        return redirect('expenses')
    
    return render(request,"project_new_expenses.html")