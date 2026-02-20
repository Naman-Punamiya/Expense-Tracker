from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from django.utils.timezone import now
from .models import Investment


def investment(request):

    # ================= SEARCH + FILTER =================
    query = request.GET.get('q')
    currency = request.GET.get('currency')
    # ===================================================

    investments = Investment.objects.all().order_by('-date')

    # 🔍 Search filter
    if query:
        investments = investments.filter(
            Q(investmentName__icontains=query) |
            Q(description__icontains=query) |
            Q(currency__icontains=query)
        )

    # 💱 Currency filter
    if currency:
        investments = investments.filter(currency=currency)

    # Unique currencies for dropdown
    currencies = Investment.objects.values_list('currency', flat=True).distinct()

    # ===== TOTAL INVESTMENT =====
    total_investments = investments.aggregate(total=Sum('amount'))['total'] or 0

    # ===== MONTHLY INVESTMENT =====
    today = now()
    monthly_investments = investments.filter(
        date__year=today.year,
        date__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0

    context = {
        "investments": investments,
        "total_investments": total_investments,
        "monthly_investments": monthly_investments,
        "currencies": currencies,   # ✅ for dropdown
    }

    return render(request, "project_investment.html", context)


def add_investment(request):

    if request.method == "POST":
        Investment.objects.create(
            investmentName=request.POST.get('name'),
            date=request.POST.get('date'),
            amount=request.POST.get('amount'),
            currency=request.POST.get('currency'),
            description=request.POST.get('description'),
        )
        return redirect('investment')

    return render(request, "project_new_investment.html")


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


def delete_investment(request, id):

    inv = get_object_or_404(Investment, id=id)

    if request.method == "POST":
        inv.delete()

    return redirect('investment')