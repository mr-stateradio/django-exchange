# -*- coding: utf-8 -*-

from django.db import models
import datetime

class Currency(models.Model):
    """Model holds a currency information for a nationality"""
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=64)

    class Meta:
        ordering = ['code']

    def __unicode__(self):
        return self.code


class ExchangeRate(models.Model):
    """Model to persist the latest exchange rates between currencies.
       regularly updated via management command 'update_exchange_rates'"""
    source = models.ForeignKey('exchange.Currency', related_name='rates')
    target = models.ForeignKey('exchange.Currency')
    timestamp = models.DateTimeField()
    rate = models.DecimalField(max_digits=14, decimal_places=4)

    def __unicode__(self):
        return '%s / %s / %s = %s' % (self.source, self.target, self.timestamp, self.rate)


class ExchangeRateHistorical(models.Model):
    """Model to persist historical exchange rates between currencies.
       updated on a per-request basis"""
    source = models.ForeignKey('exchange.Currency', related_name='historical_rates')
    target = models.ForeignKey('exchange.Currency')
    date = models.DateField()
    rate = models.DecimalField(max_digits=14, decimal_places=4)

    def __unicode__(self):
        return '%s / %s / %s = %s' % (self.source, self.target, self.date, self.rate)

    class Meta:
        unique_together = ('source', 'target', 'date')
