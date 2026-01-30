from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
from expenses.models import Expense

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    expenses = Expense.objects.all()
    total = sum(e.amount for e in expenses)
    return render(request,'project_homepage.html',{'total' : total})

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
    return render(request,'project_login.html')