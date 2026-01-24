from django.shortcuts import render

def home(request):
    return render(request,'project_homepage.html')

def investment(request):
    return render(request,'project_investment.html')

def settings(request):
    return render(request,'project_settings.html')
