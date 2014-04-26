# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Place'
        db.create_table(u'diffusion_place', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='places', to=orm['people.Organization'])),
        ))
        db.send_create_signal(u'diffusion', ['Place'])

        # Adding model 'Award'
        db.create_table(u'diffusion_award', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'diffusion', ['Award'])


    def backwards(self, orm):
        # Deleting model 'Place'
        db.delete_table(u'diffusion_place')

        # Deleting model 'Award'
        db.delete_table(u'diffusion_award')


    models = {
        u'diffusion.award': {
            'Meta': {'object_name': 'Award'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'diffusion.place': {
            'Meta': {'object_name': 'Place'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'places'", 'to': u"orm['people.Organization']"})
        },
        u'people.organization': {
            'Meta': {'object_name': 'Organization'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['diffusion']