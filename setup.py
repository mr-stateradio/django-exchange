from distutils.core import setup

setup(
    name='django-exchange',
    packages=['exchange', 'exchange.adapters', 'exchange.adapters.tests', 'exchange.management', 'exchange.management.commands'],
    provides = ['exchange'],
    version='0.0.2',
    description='currency, exchange rates and conversions support for django',
    author='Metglobal',
    author_email='kadir.pekel@metglobal.com',
    url='https://github.com/metglobal/django-exchange'
)
