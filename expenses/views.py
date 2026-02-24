from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from django.utils.timezone import now
from datetime import date
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Categories, Expense, Account


# ================= ADD EXPENSE =================
def add_expenses(request):

    account = request.user.account_set.first()

    if request.method == "POST":
        Expense.objects.create(
            account=account,
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

    account = request.user.account_set.first()

    query = request.GET.get('q')
    category = request.GET.get('category')

    all_expenses = Expense.objects.filter(
        account=account
    ).order_by('-date')

    # 🔍 SEARCH
    if query:
        all_expenses = all_expenses.filter(
            expenseName__icontains=query
        )

    # 📂 CATEGORY FILTER
    if category:
        all_expenses = all_expenses.filter(
            category=category
        )

    # ===== TOTAL =====
    total_expenses = all_expenses.aggregate(
        total=Sum('amount')
    )['total'] or 0

    today = now()

    monthly_expenses = all_expenses.filter(
        date__year=today.year,
        date__month=today.month
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    context = {
        "expenses": all_expenses,
        "total_expenses": total_expenses,
        "monthly_expenses": monthly_expenses,
        "categories": Expense.objects.filter(
            account=account
        ).values_list('category', flat=True).distinct(),
    }

    return render(request, "project_expenses.html", context)


# ================= EDIT EXPENSE =================
def edit_expense(request, id):

    account = request.user.account_set.first()

    expense = get_object_or_404(
        Expense,
        id=id,
        account=account
    )

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


# ================= DELETE EXPENSE =================
def delete_expense(request, id):

    account = request.user.account_set.first()

    expense = get_object_or_404(
        Expense,
        id=id,
        account=account
    )

    if request.method == "POST":
        expense.delete()

    return redirect('expenses')

def add_member(request):

    if request.method == "POST":
        email = request.POST.get("email")

        try:
            new_user = User.objects.get(email=email)

            account = request.user.account_set.first()

            if new_user not in account.members.all():
                account.members.add(new_user)
                messages.success(request, "Member added successfully!")

        except User.DoesNotExist:
            messages.error(request, "User with this email not found.")

    return redirect("settings")