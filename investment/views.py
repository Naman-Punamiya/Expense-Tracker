from django.shortcuts import redirect, render, get_object_or_404
from .models import Investment

<<<<<<< Updated upstream
# ---------------- CREATE ----------------
=======


def investment(request):
    
    from django.db.models import Q
    from django.db.models import Sum
    from django.utils.timezone import now

    query = request.GET.get('q')            # search
    currency = request.GET.get('currency')  # currency filter  ✅ NEW

    investments = Investment.objects.all().order_by('-date')

    # ================= SEARCH FILTER =================
    if query:
        investments = investments.filter(
            Q(investmentName__icontains=query) |
            Q(description__icontains=query) |
            Q(currency__icontains=query)
        )

    # ================= CURRENCY FILTER =================
    if currency:   # ✅ NEW
        investments = investments.filter(currency=currency)

    # ===== TOTAL INVESTMENT =====
    total_investments = (
        investments.aggregate(
            total=Sum('amount')
        )['total'] or 0
    )

    # ===== MONTHLY INVESTMENT =====
    today = now()

    monthly_investments = (
        investments.filter(
            date__year=today.year,
            date__month=today.month
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0
    )

    # ===== DISTINCT CURRENCIES FOR DROPDOWN =====
    currencies = Investment.objects.values_list('currency', flat=True).distinct()  # ✅ NEW

    context = {
        "investments": investments,
        "total_investments": total_investments,
        "monthly_investments": monthly_investments,
        "currencies": currencies,   # ✅ NEW
    }

    return render(
        request,
        "project_investment.html",
        context
    )


>>>>>>> Stashed changes
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