from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.utils.timezone import now
from datetime import date
from django.db.models import Q
from .models import Categories, Expense


# ================= ADD EXPENSE =================
def add_expenses(request):

    if request.method == "POST":
        Expense.objects.create(
            user=request.user,   # ✅ ADD
            expenseName=request.POST.get('name'),
            category=request.POST.get('category'),
            date=request.POST.get('date'),
            amount=request.POST.get('amount'),
            currency=request.POST.get('currency'),
            description=request.POST.get('description'),
        )
        return redirect('expenses')

    context = {
        "categories": Categories,
        "today": date.today().isoformat()
    }

    return render(request, "project_new_expenses.html", context)


# ================= EXPENSE LIST =================
def expenses(request):

    query = request.GET.get('q')          # expense name search
    category = request.GET.get('category')

    # all_expenses = Expense.objects.all().order_by('-date')
    all_expenses = Expense.objects.filter(user=request.user).order_by('-date')   # ✅

    # 🔍 SEARCH (ONLY expense name)
    if query:
        all_expenses = all_expenses.filter(
            Q(expenseName__icontains=query)
        )

    # 📂 CATEGORY FILTER
    if category:
        all_expenses = all_expenses.filter(category=category)

    # totals
    total_expenses = all_expenses.aggregate(
        total=Sum('amount')
    )['total'] or 0

    today = now()

    monthly_expenses = all_expenses.filter(
        date__year=today.year,
        date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0

    context = {
        "expenses": all_expenses,
        "total_expenses": total_expenses,
        "monthly_expenses": monthly_expenses,
        # "categories": Expense.objects.values_list('category', flat=True).distinct(),
        "categories": Expense.objects.filter(user=request.user)
               .values_list('category', flat=True).distinct(),  # dropdown
    }

    return render(request, "project_expenses.html", context)

# ================= EDIT =================
def edit_expense(request, id):

    # expense = get_object_or_404(Expense, id=id)
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == "POST":
        expense.expenseName = request.POST.get('expenseName')
        expense.category = request.POST.get('category')
        expense.amount = request.POST.get('amount')
        expense.currency = request.POST.get('currency')
        expense.date = request.POST.get('date')

        expense.save()

        return redirect('expenses')

    return render(
        request,
        "edit_expense.html",
        {"expense": expense}
    )


# ================= DELETE =================
def delete_expense(request, id):

    # expense = get_object_or_404(Expense, id=id)
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == "POST":
        expense.delete()

    return redirect('expenses')
