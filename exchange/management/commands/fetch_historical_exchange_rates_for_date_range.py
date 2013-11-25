# -*- coding: utf-8 -*-

from datetime import datetime, date
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from exchange.utils import import_class, daterange
from exchange.adapters import BaseAdapter
from exchange.models import Currency, ExchangeRateHistorical


class Command(BaseCommand):
    """This command triggers any
    :py:class:`exchange.adapters.BaseAdapter` implementation given by
    ``class`` option
    start_date and end_date have to be provided as args
    if today option is provided start_date and end_date is set to todays date

    """
    option_list = BaseCommand.option_list + (
        make_option(
            '-c', '--class', dest='class', help='adapter class',
            default='exchange.adapters.'
                    'openexchangerates.OpenExchangeRatesAdapter'
        ),
        make_option('--today',
            action='store_true',
            help='If this option is provided exchange rates for today will be fetched.'),
        make_option('--startdate', dest='startdate',
                    help='Please provide a start date in the format YYYY-MM-DD'),
        make_option('--enddate', dest='enddate',
                    help='Please provide an end date in the format YYYY-MM-DD'),
    )

    def handle(self, *args, **options):
        """
        Handle command
        """
        date_format = "%Y-%m-%d"
        adapter_class_name = options['class']
        execute_update = True
        # make sure file option is present
        if options.get('today', False):
            start_date = date.today()
            end_date = date.today()
            #check if all exchange rates for today are already present - if yes - cancel thread
            curr_count = Currency.objects.all().count()
            target_number = curr_count * curr_count
            exchange_rate_count = ExchangeRateHistorical.objects.filter(date=start_date).count()
            if target_number == exchange_rate_count:
                #cancel termination - all exchange rates already available
                execute_update = False
        else:
            if options['startdate'] == None :
                raise CommandError("Option `--startdate=...` must be provided.")
            else:
                #check format of input
                try:
                    start_date = datetime.strptime(options['startdate'], date_format).date()
                except Exception, e:
                    raise CommandError("Option `--startdate=...` must be provided in the format YYYY-MM-DD.")
            if options['enddate'] == None :
                raise CommandError("Option `--enddate=...` must be provided.")
            else:
                #check format of input
                try:
                    end_date = datetime.strptime(options['enddate'], date_format).date()
                except:
                    raise CommandError("Option `--enddate=...` must be specified in the format YYYY-MM-DD.")

        try:
            adapter_class = import_class(adapter_class_name)
            adapter = adapter_class()
            if not isinstance(adapter, BaseAdapter):
                raise TypeError
        except (ImportError, TypeError), detail:
            raise CommandError("invalid adapter class: Detail: %s" % detail)
        for arg in args:
            start_date, end_date = arg, None
            try:
                first_name, last_name = arg.split('.')
            except ValueError:
                first_name, last_name = arg, None

        if execute_update == True:
            currencies = Currency.objects.all()
            if len(currencies) == 0:
                raise CommandError("No currencies setup in database. You have to run the update_exchange_rate management command prior to running this command.")
            
            #for each day in date range call update_historical_exchange_rates
            for curr_date in daterange(start_date, end_date, mode=1):
                for source in currencies:
                    adapter.update_historical_exchange_rates(source, curr_date)
