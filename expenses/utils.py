from .models import Account


def get_active_account(request):

    account_id = request.session.get("account_id")

    # ✅ Try session account
    if account_id:
        try:
            return Account.objects.get(
                id=account_id,
                members=request.user   # 🔐 SECURITY CHECK
            )
        except Account.DoesNotExist:
            pass

    # ✅ fallback → first allowed account
    account = request.user.account_set.first()

    if account:
        request.session["account_id"] = account.id

    return account