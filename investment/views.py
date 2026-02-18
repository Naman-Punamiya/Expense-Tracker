from django.shortcuts import redirect, render
from .models import Investment

# Create your views here.
def add_investment(request):
    if request.method == "POST":
        Investment.objects.create(
            investmentName = request.POST.get('name'),
            date = request.POST.get('date'),
            amount = request.POST.get('amount'),
            currency = request.POST.get('currency'),
            description = request.POST.get('description'),
        )
        return redirect('investment')
    
    return render(request,"project_new_investment.html")

def investment(request):
    all_investment = Investment.objects.all().order_by('-date')
    return render(request,'project_investment.html',{'investments' : all_investment})

def newInvestment(request):
    return render(request,'project_new_investment.html')