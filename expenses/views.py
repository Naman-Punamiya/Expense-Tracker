from django.shortcuts import get_object_or_404, render,redirect
from .models import Categories, Expense
from datetime import date
from django.db.models import Sum
from django.utils.timezone import now


def add_expenses(request):
    if request.method == "POST":
        Expense.objects.create(
            expenseName = request.POST.get('name'),
            category = request.POST.get('category'),
            date = request.POST.get('date'),
            amount = request.POST.get('amount'),
            currency = request.POST.get('currency'),
            description = request.POST.get('description'),
        )
        return redirect('expenses')
    
    context = {
        "categories": Categories,
        "today": date.today().isoformat()
    }
    
    return render(request,"project_new_expenses.html",context)

def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id)

    if request.method == "POST":
        expense.delete()
        return redirect('expenses')

    return redirect('expenses')

def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id)

    if request.method == "POST":
        expense.expenseName = request.POST.get('expenseName')
        expense.category = request.POST.get('category')
        expense.amount = request.POST.get('amount')
        expense.currency = request.POST.get('currency')
        expense.date = request.POST.get('date')

        expense.save()
        return redirect('expenses')  # back to expense list

    return render(request, 'edit_expense.html', {'expense': expense})


def expenses(request):
    all_expenses = Expense.objects.all().order_by('-date')
    total_expenses = Expense.objects.aggregate(
        total = Sum('amount')
        )['total'] or 0
    
    today = now()
    monthly_expenses = Expense.objects.filter(
        date__year=today.year, 
        date__month=today.month
        ).aggregate(total = Sum('amount'))['total'] or 0
    
    context = {
        'expenses': all_expenses,
        'total_expenses': total_expenses,
        'monthly_expenses': monthly_expenses
    }
    return render(request,'project_expenses.html',context)

def newExpenses(request):
    return render(request,'project_new_expenses.html')

def expense_detail(request, id):
    expense = get_object_or_404(Expense, id=id)
    return render(request, 'expense_detail.html', {'expense': expense})