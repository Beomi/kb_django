from django.http import JsonResponse
from django.conf import settings
from core.functions import get_balance

from .models import Transaction


def balance_json(request):
    transaction_list = get_balance(
        settings.IE_DRIVER_PATH,
        settings.BANK_ACCOUNT,
        settings.BANK_PW,
        settings.BIRTHDAY
    )
    recentest_data = Transaction.objects.first()
    for trs in reversed(transaction_list):
        if not recentest_data:
            Transaction(
                date=trs['date'],
                amount=trs['amount'],
                balance=trs['balance'],
                transaction_by=trs['transaction_by'],
            ).save()
        else:
            if trs['date'] > recentest_data.date:
                Transaction(
                    date=trs['date'],
                    amount=trs['amount'],
                    balance=trs['balance'],
                    transaction_by=trs['transaction_by'],
                ).save()
    return JsonResponse(dict(data=transaction_list))
