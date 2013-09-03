# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Currency'
        db.create_table(u'exchange_currency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'exchange', ['Currency'])

        # Adding model 'ExchangeRate'
        db.create_table(u'exchange_exchangerate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rates', to=orm['exchange.Currency'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exchange.Currency'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('rate', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
        ))
        db.send_create_signal(u'exchange', ['ExchangeRate'])

        # Adding model 'ExchangeRateHistorical'
        db.create_table(u'exchange_exchangeratehistorical', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='historical_rates', to=orm['exchange.Currency'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exchange.Currency'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('rate', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=4)),
        ))
        db.send_create_signal(u'exchange', ['ExchangeRateHistorical'])

        # Adding unique constraint on 'ExchangeRateHistorical', fields ['source', 'target', 'date']
        db.create_unique(u'exchange_exchangeratehistorical', ['source_id', 'target_id', 'date'])


    def backwards(self, orm):
        # Removing unique constraint on 'ExchangeRateHistorical', fields ['source', 'target', 'date']
        db.delete_unique(u'exchange_exchangeratehistorical', ['source_id', 'target_id', 'date'])

        # Deleting model 'Currency'
        db.delete_table(u'exchange_currency')

        # Deleting model 'ExchangeRate'
        db.delete_table(u'exchange_exchangerate')

        # Deleting model 'ExchangeRateHistorical'
        db.delete_table(u'exchange_exchangeratehistorical')


    models = {
        u'exchange.currency': {
            'Meta': {'ordering': "['code']", 'object_name': 'Currency'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'exchange.exchangerate': {
            'Meta': {'object_name': 'ExchangeRate'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rates'", 'to': u"orm['exchange.Currency']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exchange.Currency']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'exchange.exchangeratehistorical': {
            'Meta': {'unique_together': "(('source', 'target', 'date'),)", 'object_name': 'ExchangeRateHistorical'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '4'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'historical_rates'", 'to': u"orm['exchange.Currency']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['exchange.Currency']"})
        }
    }

    complete_apps = ['exchange']