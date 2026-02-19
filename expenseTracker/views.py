<<<<<<< HEAD
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
from expenses.models import Expense

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    expenses = Expense.objects.all()
    total = sum(e.amount for e in expenses)
    return render(request,'project_homepage.html',{'total' : total})
=======
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
from expenses.models import Expense
from django.shortcuts import render
from django.db.models import Sum
from expenses.models import Expense
from investment.models import Investment
from django.db.models import Count

def home(request):
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    recent_expenses = Expense.objects.order_by('-date')[:4]
    recent_investments = Investment.objects.order_by('-date')[:4]

    expense_distribution = (
        Expense.objects
        .values('category')
        .annotate(total=Sum('amount'))
    )

    expenses_labels = [item['category'] for item in expense_distribution]
    expenses_data = [float(item['total']) for item in expense_distribution]

    # investment_distribution = (
    #     Investment.objects
    #     .values('investmentName')
    #     .annotate(total=Sum('amount'))
    # )

    # investments_labels = [item['investmentName'] for item in investment_distribution]
    # investments_data = [float(item['total']) for item in investment_distribution]

    context = {
        "recent_expenses": recent_expenses,
        "recent_investments": recent_investments,
        "expenses_labels": expenses_labels,
        "expenses_data": expenses_data,
        # "investments_labels": investments_labels,
        # "investments_data": investments_data,
    }

    # expenses = Expense.objects.all()
    # total = sum(e.amount for e in expenses)
    return render(request,'project_homepage.html',context)
>>>>>>> origin/naman

def investment(request):
    return render(request,'project_investment.html')

def settings(request):
    return render(request,'project_settings.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username = username , password = password)
        if user is not None:
            login(request , user)
            return redirect("home")
        else:
            return render(request, "project_login.html", {
                "error": "Invalid username or password"
            })
<<<<<<< HEAD
    return render(request,'project_login.html')
=======
    return render(request,'project_login.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "project_register.html", {
                "error": "Username already exists"
            })

        if User.objects.filter(email=email).exists():
            return render(request, "project_register.html", {
                "error": "Email already exists"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect("home")

    return render(request, "project_register.html")
>>>>>>> origin/naman
