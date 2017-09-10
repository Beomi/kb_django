import pytz

from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from core.functions import get_balance

from .models import Transaction

local_tz = pytz.timezone('Asia/Seoul')

def balance_json(request):
    transaction_list = get_balance(
        settings.IE_DRIVER_PATH,
        settings.BANK_ACCOUNT,
        settings.BANK_PW,
        settings.BIRTHDAY
    )
    latest_data = Transaction.objects.last()
    for trs in reversed(transaction_list):
        if not latest_data:
            Transaction(
                date=trs['date'],
                amount=trs['amount'],
                balance=trs['balance'],
                transaction_by=trs['transaction_by'],
            ).save()
        else:
            if trs['date'].replace(tzinfo=local_tz) > latest_data.date:
                Transaction(
                    date=trs['date'],
                    amount=trs['amount'],
                    balance=trs['balance'],
                    transaction_by=trs['transaction_by'],
                ).save()
    return JsonResponse(dict(data=transaction_list))
