from .models import Account

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