from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.utils.timezone import now
from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Category, Expense, Account


# ================= GET OR CREATE ACCOUNT =================
def get_user_account(user):
    account = user.account_set.first()

    if not account:
        account = Account.objects.create(
            name=f"{user.username} Account"
        )
        account.members.add(user)

    return account


# ================= ADD EXPENSE =================
@login_required
def add_expenses(request):

    account = get_user_account(request.user)

    if request.method == "POST":
        Expense.objects.create(
            account=account,
            expenseName=request.POST.get("name"),
            category_id=request.POST.get("category"),
            date=request.POST.get("date"),
            amount=request.POST.get("amount"),
            currency=request.POST.get("currency"),
            description=request.POST.get("description"),
        )

        messages.success(request, "Expense added successfully!")
        return redirect("expenses")

    context = {
        "categories": Category.objects.all(),
        "today": date.today().isoformat(),
    }

    return render(request, "project_new_expenses.html", context)


# ================= EXPENSE LIST =================
@login_required
def expenses(request):

    account = get_user_account(request.user)

    query = request.GET.get("q")
    category = request.GET.get("category")

    all_expenses = Expense.objects.filter(
        account=account
    ).order_by("-date")

    # SEARCH
    if query:
        all_expenses = all_expenses.filter(
            expenseName__icontains=query
        )

    # CATEGORY FILTER
    if category:
        all_expenses = all_expenses.filter(
            category_id=category
        )

    # TOTAL EXPENSES
    total_expenses = all_expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0

    today = now()

    # MONTHLY EXPENSES
    monthly_expenses = all_expenses.filter(
        date__year=today.year,
        date__month=today.month
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    context = {
        "expenses": all_expenses,
        "total_expenses": total_expenses,
        "monthly_expenses": monthly_expenses,
        "categories": Category.objects.all(),
    }

    return render(request, "project_expenses.html", context)


# ================= EDIT EXPENSE =================
@login_required
def edit_expense(request, id):

    account = get_user_account(request.user)

    expense = get_object_or_404(
        Expense,
        id=id,
        account=account
    )

    if request.method == "POST":
        expense.expenseName = request.POST.get("expenseName")
        expense.category_id = request.POST.get("category")
        expense.amount = request.POST.get("amount")
        expense.currency = request.POST.get("currency")
        expense.date = request.POST.get("date")

        expense.save()

        messages.success(request, "Expense updated successfully!")
        return redirect("expenses")

    context = {
        "expense": expense,
        "categories": Category.objects.all(),
    }

    return render(request, "edit_expense.html", context)


# ================= DELETE EXPENSE =================
@login_required
def delete_expense(request, id):

    account = get_user_account(request.user)

    expense = get_object_or_404(
        Expense,
        id=id,
        account=account
    )

    if request.method == "POST":
        expense.delete()
        messages.success(request, "Expense deleted successfully!")

    return redirect("expenses")


# ================= ADD MEMBER =================
@login_required
def add_member(request):

    if request.method == "POST":

        email = request.POST.get("email")

        try:
            new_user = User.objects.get(email=email)

            account = get_user_account(request.user)

            if new_user not in account.members.all():
                account.members.add(new_user)
                messages.success(request, "Member added successfully!")

            else:
                messages.warning(request, "User is already a member.")

        except User.DoesNotExist:
            messages.error(request, "User with this email not found.")

    return redirect("settings")