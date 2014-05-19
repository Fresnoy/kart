# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BTBeacon'
        db.create_table(u'common_btbeacon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('uuid', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32)),
        ))
        db.send_create_signal(u'common', ['BTBeacon'])


    def backwards(self, orm):
        # Deleting model 'BTBeacon'
        db.delete_table(u'common_btbeacon')


    models = {
        u'common.btbeacon': {
            'Meta': {'object_name': 'BTBeacon'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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