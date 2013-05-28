from django.contrib import admin
from models import Currency, ExchangeRate, ExchangeRateHistorical

admin.site.register(Currency)
admin.site.register(ExchangeRate)
admin.site.register(ExchangeRateHistorical)