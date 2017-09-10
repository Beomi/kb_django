from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from core.functions import get_balance

from .models import Transaction

def balance_json(request):
    transaction_list = get_balance(
        settings.IE_DRIVER_PATH,
        settings.BANK_ACCOUNT,
        settings.BANK_PW,
        settings.BIRTHDAY
    )
    latest_data = Transaction.objects.last()
    if not latest_data:
        latest_data['date'] = timezone.now()
    for trs in transaction_list:
        if trs['date'] > latest_data.date:
            Transaction(
                date=trs['date'],
                amount=trs['amount'],
                balance=trs['balance'],
                transaction_by=trs['transaction_by'],
            ).save()
    return JsonResponse(data=transaction_list)
