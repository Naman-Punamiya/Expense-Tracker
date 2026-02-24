from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Sum

from expenses.models import Expense
from investment.models import Investment


# ================= HOME DASHBOARD =================
def home(request):

    if not request.user.is_authenticated:
        return redirect('login')

    # ✅ shared account
    account = request.user.account_set.first()

    # ---------- Recent Records ----------
    recent_expenses = Expense.objects.filter(
        account=account
    ).order_by('-date')[:4]

    recent_investments = Investment.objects.filter(
        account=account
    ).order_by('-date')[:4]

    # ---------- Expense Chart ----------
    expense_distribution = (
        Expense.objects
        .filter(account=account)
        .values('category')
        .annotate(total=Sum('amount'))
    )

    expenses_labels = [
        item['category']
        for item in expense_distribution
    ]

    expenses_data = [
        float(item['total'])
        for item in expense_distribution
    ]

    # ---------- Investment Chart ----------
    investment_distribution = (
        Investment.objects
        .filter(account=account)
        .values('investmentName')
        .annotate(total=Sum('amount'))
    )

    investment_labels = [
        item['investmentName']
        for item in investment_distribution
    ]

    investment_data = [
        float(item['total'])
        for item in investment_distribution
    ]

    context = {
        "recent_expenses": recent_expenses,
        "recent_investments": recent_investments,
        "expenses_labels": expenses_labels,
        "expenses_data": expenses_data,
        "investment_labels": investment_labels,
        "investment_data": investment_data,
    }

    return render(request, "project_homepage.html", context)


# ================= SETTINGS =================
def settings(request):
    return render(request, 'project_settings.html')


# ================= LOGIN =================
def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(
            request,
            "project_login.html",
            {"error": "Invalid username or password"}
        )

    return render(request, 'project_login.html')


# ================= REGISTER =================
def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "project_register.html",
                {"error": "Username already exists"}
            )

        if User.objects.filter(email=email).exists():
            return render(
                request,
                "project_register.html",
                {"error": "Email already exists"}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect("home")

    return render(request, "project_register.html")