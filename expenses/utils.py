from .models import Account

# Currency conversion rates
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

# FUNCTION: Get the currently active account
def get_active_account(request):
    account_id = request.session.get("account_id")
    if account_id:
        try:
            return Account.objects.get(
                id=account_id,
                members=request.user
            )
        except Account.DoesNotExist:
            pass


    # STEP 2: If no session account exists
    account = request.user.account_set.first()
    if account:
        request.session["account_id"] = account.id
    return account