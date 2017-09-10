from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    fields = ('date', 'amount', 'balance', 'transaction_by', )
    ordering = '-date'
