from django.shortcuts import render,redirect
from .models import Expense

def add_expenses(request):
    if request.method == "POST":
        Expense.objects.create(
            expenseName = request.POST.get('name'),
            date = request.POST.get('date'),
            amount = request.POST.get('amount'),
            currency = request.POST.get('currency'),
            description = request.POST.get('description'),
        )
        return redirect('expenses')
    
    return render(request,"project_new_expenses.html")

def expenses(request):
    all_expenses = Expense.objects.all().order_by('-date')
    return render(request,'project_expenses.html',{'expenses' : all_expenses})

def newExpenses(request):
    return render(request,'project_new_expenses.html')