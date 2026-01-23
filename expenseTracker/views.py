from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request,'project_homepage.html')

def expenses(request):
    return render(request,'project_expenses.html')

def investment(request):
    return render(request,'project_investment.html')

def settings(request):
    return render(request,'project_settings.html')

def newExpenses(request):
    return render(request,'project_new_expenses.html')
