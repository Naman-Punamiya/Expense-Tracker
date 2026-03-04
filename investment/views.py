from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from django.utils.timezone import now

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Investment
from expenses.models import Account


# ================= GET USER ACCOUNT =================
def get_user_account(user):

    account = user.account_set.first()

    if not account:
        account = Account.objects.create(
            name=f"{user.username} Account"
        )
        account.members.add(user)

    return account


# ================= INVESTMENT LIST =================
@login_required
def investment(request):

    account = get_user_account(request.user)

    # ===== SEARCH + FILTER =====
    query = request.GET.get("q")
    currency = request.GET.get("currency")

    investments = Investment.objects.filter(
        account=account
    ).order_by("-date")

    # 🔍 SEARCH
    if query:
        investments = investments.filter(
            Q(investmentName__icontains=query) |
            Q(description__icontains=query) |
            Q(currency__icontains=query)
        )

    # 💱 CURRENCY FILTER
    if currency:
        investments = investments.filter(currency=currency)

    # AVAILABLE CURRENCIES
    currencies = Investment.objects.filter(
        account=account
    ).values_list("currency", flat=True).distinct()

    # ===== TOTAL =====
    total_investments = investments.aggregate(
        total=Sum("amount")
    )["total"] or 0

    # ===== MONTHLY =====
    today = now()

    monthly_investments = investments.filter(
        date__year=today.year,
        date__month=today.month
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    context = {
        "investments": investments,
        "total_investments": total_investments,
        "monthly_investments": monthly_investments,
        "currencies": currencies,
    }

    return render(request, "project_investment.html", context)


# ================= ADD INVESTMENT =================
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


# ================= EDIT INVESTMENT =================
@login_required
def edit_investment(request, id):

    account = get_user_account(request.user)

    inv = get_object_or_404(
        Investment,
        id=id,
        account=account
    )

    if request.method == "POST":

        inv.investmentName = request.POST.get("name")
        inv.date = request.POST.get("date")
        inv.amount = request.POST.get("amount")
        inv.currency = request.POST.get("currency")
        inv.description = request.POST.get("description")

        inv.save()

        messages.success(request, "Investment updated successfully!")
        return redirect("investment")

    return render(
        request,
        "project_edit_investment.html",
        {"inv": inv}
    )


# ================= DELETE INVESTMENT =================
@login_required
def delete_investment(request, id):

    account = get_user_account(request.user)

    inv = get_object_or_404(
        Investment,
        id=id,
        account=account
    )

    if request.method == "POST":
        inv.delete()
        messages.success(request, "Investment deleted successfully!")

    return redirect("investment")