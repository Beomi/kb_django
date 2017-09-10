from django.db import models

class TimeStampModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Create your models here.
class Transaction(TimeStampModel):
    class Meta:
        verbose_name = '거래내역'
        verbose_name_plural = '거래내역'

    date = models.DateTimeField('거래일시')
    amount = models.IntegerField('거래금액')
    balance = models.IntegerField('잔고')
    transaction_by = models.CharField('거래소', max_length=200)

    def __str__(self):
        return '{} {}'.format(self.transaction_by, self.balance)
