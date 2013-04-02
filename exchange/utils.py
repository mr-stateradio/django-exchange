from exchange.models import Currency
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def import_class(class_path):
    """imports and returns given class string.

    :param class_path: Class path as string
    :type class_path: str

    :returns: Class that has given path
    :rtype: class

    :Example:

    >>> import_class('collections.OrderedDict').__name__
    'OrderedDict'
    """
    try:
        from django.utils.importlib import import_module
        module_name = '.'.join(class_path.split(".")[:-1])
        mod = import_module(module_name)
        return getattr(mod, class_path.split(".")[-1])
    except Exception, detail:
        raise ImportError(detail)
    

def daterange(start_date, end_date, mode=0):
    """
    generator returning all days between start and end date
    mode == 0 -> provides date range excluding end_date
    mode == 1 -> provides date range including end_date
    """
    if mode == 1:
        end_date += relativedelta(days=1)
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
