from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from expenses.models import Expense
from investment.models import Investment

# Currency conversion
USD_TO_INR = 83
EUR_TO_INR = 90

def convert_to_inr(amount, currency):
    amount = float(amount)

    if currency == "USD":
        return amount * USD_TO_INR
    elif currency == "EUR":
        return amount * EUR_TO_INR
    else:
        return amount

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
    investments = Investment.objects.filter(account=account)

    investment_chart = {}

    for inv in investments:
        amount_inr = convert_to_inr(inv.amount, inv.currency)

        if inv.investmentName in investment_chart:
            investment_chart[inv.investmentName] += amount_inr
        else:
            investment_chart[inv.investmentName] = amount_inr

    investment_labels = list(investment_chart.keys())
    investment_data = list(investment_chart.values())
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

    if request.method == "POST":
        user = request.user

        user.username = request.POST.get("full_name")
        user.email = request.POST.get("email")

        password = request.POST.get("password")
        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)

        user.save()

        messages.success(request, "Settings updated successfully!")

        return redirect("settings")

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