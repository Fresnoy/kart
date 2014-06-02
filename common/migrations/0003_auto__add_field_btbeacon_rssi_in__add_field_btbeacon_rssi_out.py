# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'BTBeacon.rssi_in'
        db.add_column(u'common_btbeacon', 'rssi_in',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'BTBeacon.rssi_out'
        db.add_column(u'common_btbeacon', 'rssi_out',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'BTBeacon.rssi_in'
        db.delete_column(u'common_btbeacon', 'rssi_in')

        # Deleting field 'BTBeacon.rssi_out'
        db.delete_column(u'common_btbeacon', 'rssi_out')


    models = {
        u'common.btbeacon': {
            'Meta': {'object_name': 'BTBeacon'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rssi_in': ('django.db.models.fields.IntegerField', [], {}),
            'rssi_out': ('django.db.models.fields.IntegerField', [], {}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'common.website': {
            'Meta': {'object_name': 'Website'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['common']