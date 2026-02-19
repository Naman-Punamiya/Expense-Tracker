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


# ---------------- READ ----------------
def investment(request):
    all_investment = Investment.objects.all().order_by('-date')
    return render(request,'project_investment.html',{'investments' : all_investment})


# ---------------- UPDATE ----------------
def edit_investment(request, id):
    inv = get_object_or_404(Investment, id=id)

    if request.method == "POST":
        inv.investmentName = request.POST.get('name')
        inv.date = request.POST.get('date')
        inv.amount = request.POST.get('amount')
        inv.currency = request.POST.get('currency')
        inv.description = request.POST.get('description')
        inv.save()
        return redirect('investment')

    return render(request, 'project_edit_investment.html', {'inv': inv})


# ---------------- DELETE ----------------
def delete_investment(request, id):
    inv = get_object_or_404(Investment, id=id)
    inv.delete()
    return redirect('investment')
def newInvestment(request):
    return render(request,'project_new_investment.html')
