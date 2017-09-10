from django.conf.urls import url

from .views import balance_json

urlpatterns = [
    url('', balance_json, name='balance_json'),
]
