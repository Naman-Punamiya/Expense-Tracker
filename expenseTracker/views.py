from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from expenses.models import Expense
from investment.models import Investment

# HOME DASHBOARD
@login_required
def home(request):
    account = request.user.account_set.first()
    recent_expenses = Expense.objects.filter(
        account=account
    ).order_by("-date")[:4]
    recent_investments = Investment.objects.filter(
        account=account
    ).order_by("-date")[:4]
    # EXPENSE CHART DATA
    expense_distribution = (
        Expense.objects
        .filter(account=account)
        .values("category__name")
        .annotate(total=Sum("amount"))
    )
    expenses_labels = [
        item["category__name"]
        for item in expense_distribution
    ]
    expenses_data = [
        float(item["total"])
        for item in expense_distribution
    ]
    # INVESTMENT CHART DATA
    investment_distribution = (
        Investment.objects
        .filter(account=account)
        .values("investmentName")
        .annotate(total=Sum("amount"))
    )
    investment_labels = [
        item["investmentName"]
        for item in investment_distribution
    ]
    investment_data = [
        float(item["total"])
        for item in investment_distribution
    ]
    # Data sent to the HTML template
    context = {
        "recent_expenses": recent_expenses,
        "recent_investments": recent_investments,
        "expenses_labels": expenses_labels,
        "expenses_data": expenses_data,
        "investment_labels": investment_labels,
        "investment_data": investment_data,
    }
    return render(request, "project_homepage.html", context)


# SETTINGS PAGE
@login_required
def settings(request):
    return render(request, "project_settings.html")


# LOGIN PAGE
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user:
            login(request, user)
            return redirect("home")
        return render(
            request,
            "project_login.html",
            {"error": "Invalid username or password"}
        )
    return render(request, "project_login.html")

# REGISTER PAGE
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(
                request,
                "project_register.html",
                {"error": "Username already exists"}
            )
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(
                request,
                "project_register.html",
                {"error": "Email already exists"}
            )
        # Create new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        # Automatically log in the new user
        login(request, user)
        return redirect("home")
    return render(request, "project_register.html")