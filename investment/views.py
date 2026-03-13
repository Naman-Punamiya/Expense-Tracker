from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Investment
from expenses.models import Account

# Currency conversion rates (example)
USD_TO_INR = 92.47
EUR_TO_INR = 106.12

def convert_to_inr(amount, currency):
    amount = float(amount)

    if currency == "USD":
        return amount * USD_TO_INR
    elif currency == "EUR":
        return amount * EUR_TO_INR
    else:  # INR
        return amount

def format_inr(amount):
    return "{:,.2f}".format(amount)

# FUNCTION: Get user's account
def get_user_account(user):
    # Get the first account linked to the user
    account = user.account_set.first()
    if not account:
        account = Account.objects.create(
            name=f"{user.username} Account"
        )
        account.members.add(user)
    return account


# PAGE: Investment List
@login_required
def investment(request):
    account = get_user_account(request.user)
    search_query = request.GET.get("q")
    currency_filter = request.GET.get("currency")
    investments = Investment.objects.filter(
        account=account
    ).order_by("-date")
    if search_query:
        investments = investments.filter(
            Q(investmentName__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(currency__icontains=search_query)
        )
    if currency_filter:
        investments = investments.filter(
            currency=currency_filter
        )
    currencies = Investment.objects.filter(
        account=account
    ).values_list("currency", flat=True).distinct()
    total_investments = 0

    for inv in investments:
        total_investments += convert_to_inr(inv.amount, inv.currency)
    today = now()
    monthly_investments = 0

    monthly_data = investments.filter(
        date__year=today.year,
        date__month=today.month
    )

    for inv in monthly_data:
        monthly_investments += convert_to_inr(inv.amount, inv.currency)
    
    context = {
        "investments": investments,
        "total_investments": format_inr(total_investments),
        "monthly_investments": format_inr(monthly_investments),
        "currencies": currencies,
    }
    return render(request, "project_investment.html", context)

# PAGE: Add Investment
@login_required
def add_investment(request):
    account = get_user_account(request.user)
    if request.method == "POST":
        Investment.objects.create(
            account=account,
            investmentName=request.POST.get("name"),
            date=request.POST.get("date"),
            amount=request.POST.get("amount"),
            currency=request.POST.get("currency"),
            description=request.POST.get("description"),
        )
        messages.success(request, "Investment added successfully!")
        return redirect("investment")
    return render(request, "project_new_investment.html")


# PAGE: Edit Investment
@login_required
def edit_investment(request, id):
    account = get_user_account(request.user)
    investment = get_object_or_404(
        Investment,
        id=id,
        account=account
    )
    if request.method == "POST":
        investment.investmentName = request.POST.get("name")
        investment.date = request.POST.get("date")
        investment.amount = request.POST.get("amount")
        investment.currency = request.POST.get("currency")
        investment.description = request.POST.get("description")
        investment.save()
        messages.success(request, "Investment updated successfully!")
        return redirect("investment")
    return render(
        request,
        "project_edit_investment.html",
        {"inv": investment}
    )

# PAGE: Delete Investment
@login_required
def delete_investment(request, id):
    account = get_user_account(request.user)
    investment = get_object_or_404(
        Investment,
        id=id,
        account=account
    )
    if request.method == "POST":
        investment.delete()
        messages.success(request, "Investment deleted successfully!")
    return redirect("investment")