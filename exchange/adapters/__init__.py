import logging
import datetime

from django.utils.timezone import make_aware, utc
 
from exchange.models import Currency, ExchangeRate, ExchangeRateHistorical

logger = logging.getLogger(__name__)


class BaseAdapter(object):
    """Base adapter class provides an interface for updating currency and
    exchange rate models

    """
    def update(self):
        """Actual update process goes here using auxiliary ``get_currencies``
        and ``get_exchangerates`` methods. This method creates or updates
        corresponding ``Currency`` and ``ExchangeRate`` models
        """
        currencies = self.get_currencies()
        for code, name in currencies:
            _, created = Currency.objects.get_or_create(
                code=code, defaults={'name': name})
            if created:
                logger.info('currency: %s created', code)

        for source in Currency.objects.all():
            exchange_rate_json = self.get_exchangerates(source.code) or []
            for code, rate in exchange_rate_json['rates'].items():
                timestamp = datetime.datetime.fromtimestamp(int(exchange_rate_json['timestamp']), tz=utc)
                try:
                    target = Currency.objects.get(code=code)
                    exchange_rate = ExchangeRate.objects.get(source=source,
                                                             target=target)
                    exchange_rate.rate = rate
                    exchange_rate.timestamp = timestamp
                    exchange_rate.save()
                    logger.info('exchange rate updated %s/%s=%s'
                                % (source, target, rate))
                except ExchangeRate.DoesNotExist:
                    exchange_rate = ExchangeRate.objects.create(
                        source=source, target=target, timestamp=timestamp, rate=rate)
                    logger.info('exchange rate created %s/%s=%s'
                                % (source, target, rate))

    def update_historical_exchange_rates(self, source, date):
        """Actual update process goes here using auxiliary ``get_historical_exchangerate``
          method. This method creates or updates corresponding ``ExchangeRateHistorical`` model
        """
        for source in Currency.objects.filter(code=source.code):
            exchange_rate_json = self.get_historical_exchangerate(source.code, date) or []
            print exchange_rate_json
            for code, rate in exchange_rate_json['rates'].items():
                date = datetime.datetime.fromtimestamp(int(exchange_rate_json['timestamp']), tz=utc)
                try:
                    target = Currency.objects.get(code=code)
                    exchange_rate = ExchangeRateHistorical.objects.get(source=source,
                                                             target=target, date=date)
                    exchange_rate.rate = rate
                    exchange_rate.save()
                    logger.info('historical exchange rate updated %s/%s/%s=%s'
                                % (source, target, date, rate))
                except ExchangeRateHistorical.DoesNotExist:
                    exchange_rate = ExchangeRateHistorical.objects.create(
                        source=source, target=target, date=date, rate=rate)
                    logger.info('historical exchange rate created %s/%s/%s=%s'
                                % (source, target, date, rate))

    def get_currencies(self):
        """Subclasses must implement this to provide all currency data

        :returns: currency tuples ``[(currency_code, currency_name),]``
        :rtype: list

        """
        raise NotImplemented()

    def get_exchangerates(self, base):
        """Subclasses must implement this to provide corresponding exchange
        rates for given base currency

        :returns: object with rates as attribute accessible via object['rates']
                  including exchange rate tuples ``[(currency_code, rate),]``
                  timestamp attribute as unix timestamp
        :rtype: json

        """
        raise NotImplemented()

    def get_historical_exchangerate(self, base, date):
        """Subclasses must implement this to provide corresponding exchange
        rates for given base currency and date

        :returns: object with rates as attribute accessible via object['rates']
                  including exchange rate tuples ``[(currency_code, rate),]``
                  timestamp attribute as unix timestamp
        :rtype: json

        """
        raise NotImplemented()
