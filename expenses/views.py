from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.utils.timezone import now
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category, Expense, Account


# FUNCTION: Get the account of the logged-in user
# If the user doesn't have an account, create one

def get_user_account(user):
    account = Account.objects.filter(members=user).first()
    if not account:
        account = Account.objects.create(
            name=f"{user.username} Account"
        )
        account.members.add(user)
    return account


# ADD EXPENSE PAGE
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


# EXPENSE LIST PAGE
@login_required
def expenses(request):
    account = get_user_account(request.user)
    # Get search inputs from URL
    search_query = request.GET.get("q")
    category_filter = request.GET.get("category")
    # Get all expenses of the account
    expense_list = Expense.objects.filter(account=account).order_by("-date")
    # Apply search filter
    if search_query:
        expense_list = expense_list.filter(
            expenseName__icontains=search_query
        )
    # Apply category filter
    if category_filter:
        try:
            expense_list = expense_list.filter(
                category_id=int(category_filter)
            )
        except (ValueError, TypeError):
            # Invalid category ID, skip filtering
            pass
    total_expenses = expense_list.aggregate(
        total=Sum("amount")
    )["total"] or 0
    today = now()
    monthly_expenses = expense_list.filter(
        date__year=today.year,
        date__month=today.month
    ).aggregate(total=Sum("amount"))["total"] or 0
    context = {
        "expenses": expense_list,
        "total_expenses": total_expenses,
        "monthly_expenses": monthly_expenses,
        "categories": Category.objects.all(),
    }
    return render(request, "project_expenses.html", context)


# EDIT EXPENSE
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
        category_id = request.POST.get("category")
        if category_id:
            expense.category_id = category_id
        else:
            expense.category = None
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


# DELETE EXPENSE
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


# ADD MEMBER TO SHARED ACCOUNT
@login_required
def add_member(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            # Find user using email
            new_user = User.objects.get(email=email)
            # Get current user's account
            account = get_user_account(request.user)
            # Add user if not already a member
            if new_user not in account.members.all():
                account.members.add(new_user)
                messages.success(request, "Member added successfully!")
            else:
                messages.warning(request, "User is already a member.")
        # If user with this email doesn't exist
        except User.DoesNotExist:
            messages.error(request, "User with this email not found.")
    return redirect("settings")