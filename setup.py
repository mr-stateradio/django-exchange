from distutils.core import setup

setup(
    name='django-exchange',
    packages=['exchange', 'exchange.adapters',  'exchange.adapters.tests', 'exchange.management', 'exchange.management.commands'],
    #package_data={
    #      'exchange': [
    #          'fixtures/initial_data.json'
    #      ],
    #  },
    provides = ['exchange'],
    version='0.2.0',
    description='currency, exchange rates and conversions support for django',
    #origin author Metglobal #originator email: kadir.pekel@metglobal.com
    url='http://github.com/mr-stateradio/django-exchange',
)
