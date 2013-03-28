from __future__ import absolute_import

import logging

from django.conf import settings

from exchange.adapters import BaseAdapter
from exchange.models import Currency, ExchangeRate

logger = logging.getLogger(__name__)



import requests

class OpenExchangeRatesClientException(requests.exceptions.RequestException):
    """Base client exception wraps all kinds of ``requests`` lib exceptions"""
    pass


class OpenExchangeRatesClient(object):
    """This class is a client implementation for openexchangerate.org service

    """
    BASE_URL = 'http://openexchangerates.org/api'
    ENDPOINT_LATEST = BASE_URL + '/latest.json'
    ENDPOINT_HISTORICAL = BASE_URL + '/historical/'
    ENDPOINT_CURRENCIES = BASE_URL + '/currencies.json'

    def __init__(self, api_key):
        """Convenient constructor"""
        self.client = requests.Session()
        self.client.params.update({'app_id': api_key})

    def latest(self, base):
        """Fetches latest exchange rate data from service

        :Example Data:
            {
                disclaimer: "<Disclaimer data>",
                license: "<License data>",
                timestamp: 1358150409,
                base: "USD",
                rates: {
                    AED: 3.666311,
                    AFN: 51.2281,
                    ALL: 104.748751,
                    AMD: 406.919999,
                    ANG: 1.7831,
                    ...
                }
            }
        """
        base='USD' #for testing purposes!! in order to use free version..only usd is supported in the free version as base
        try:
            resp = self.client.get(self.ENDPOINT_LATEST, params={'base': base})
            resp.raise_for_status()
        except requests.exceptions.RequestException, e:
            raise OpenExchangeRatesClientException(e)
        return resp.json()

    def historical(self, base, date):
        """Fetches historical exchange rate data from service"""
        base='USD' #for testing purposes!! in order to use free version..only usd is supported in the free version as base
        try:
            historical_url = self.ENDPOINT_HISTORICAL + date.strftime('%Y-%m-%d') + '.json'
            print historical_url
            resp = self.client.get(historical_url, params={'base': base})
            resp.raise_for_status()
        except requests.exceptions.RequestException, e:
            raise OpenExchangeRatesClientException(e)
        return resp.json()

    def currencies(self):
        """Fetches current currency data of the service
        :Example Data:
        {
            AED: "United Arab Emirates Dirham",
            AFN: "Afghan Afghani",
            ALL: "Albanian Lek",
            AMD: "Armenian Dram",
            ANG: "Netherlands Antillean Guilder",
            AOA: "Angolan Kwanza",
            ARS: "Argentine Peso",
            AUD: "Australian Dollar",
            AWG: "Aruban Florin",
            AZN: "Azerbaijani Manat"
            ...
        }
        """
        try:
            resp = self.client.get(self.ENDPOINT_CURRENCIES)
        except requests.exceptions.RequestException, e:
            raise OpenExchangeRatesClientException(e)
        return resp.json()


class OpenExchangeRatesAdapter(BaseAdapter):
    """This adapter uses openexchangerates.org service to populate currency and
    exchange rate models.
    """

    API_KEY_SETTINGS_KEY = 'OPENEXCHANGERATES_API_KEY'

    def __init__(self):
        self.client = OpenExchangeRatesClient(
            getattr(settings, self.API_KEY_SETTINGS_KEY))

    def get_currencies(self):
        return self.client.currencies().items()

    def get_exchangerates(self, base):
        return self.client.latest(base)
    
    def get_historical_exchangerate(self, base, date):
        return self.client.historical(base, date)
