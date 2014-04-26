# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FresnoyProfile'
        db.create_table(u'people_fresnoyprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('birthdate', self.gf('django.db.models.fields.DateField')()),
            ('birthplace', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('birthplace_country', self.gf('django_countries.fields.CountryField')(max_length=2)),
            ('homeland_address', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('homeland_country', self.gf('django_countries.fields.CountryField')(max_length=2, blank=True)),
            ('residence_address', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('residence_country', self.gf('django_countries.fields.CountryField')(max_length=2, blank=True)),
            ('homeland_phone', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('residence_phone', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('cursus', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'people', ['FresnoyProfile'])

        # Adding model 'Artist'
        db.create_table(u'people_artist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('bio_short_fr', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('bio_short_en', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('bio_fr', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('bio_en', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('twitter_account', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('facebook_profile', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'people', ['Artist'])

        # Adding M2M table for field websites on 'Artist'
        m2m_table_name = db.shorten_name(u'people_artist_websites')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artist', models.ForeignKey(orm[u'people.artist'], null=False)),
            ('website', models.ForeignKey(orm[u'common.website'], null=False))
        ))
        db.create_unique(m2m_table_name, ['artist_id', 'website_id'])

        # Adding model 'Staff'
        db.create_table(u'people_staff', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'people', ['Staff'])

        # Adding model 'Organization'
        db.create_table(u'people_organization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'people', ['Organization'])


    def backwards(self, orm):
        # Deleting model 'FresnoyProfile'
        db.delete_table(u'people_fresnoyprofile')

        # Deleting model 'Artist'
        db.delete_table(u'people_artist')

        # Removing M2M table for field websites on 'Artist'
        db.delete_table(db.shorten_name(u'people_artist_websites'))

        # Deleting model 'Staff'
        db.delete_table(u'people_staff')

        # Deleting model 'Organization'
        db.delete_table(u'people_organization')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'common.website': {
            'Meta': {'object_name': 'Website'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'people.artist': {
            'Meta': {'object_name': 'Artist'},
            'bio_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'bio_fr': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'bio_short_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'bio_short_fr': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'facebook_profile': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'twitter_account': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'websites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Website']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'people.fresnoyprofile': {
            'Meta': {'object_name': 'FresnoyProfile'},
            'birthdate': ('django.db.models.fields.DateField', [], {}),
            'birthplace': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'birthplace_country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'cursus': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'homeland_address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'homeland_country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'blank': 'True'}),
            'homeland_phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'residence_address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'residence_country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'blank': 'True'}),
            'residence_phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'people.organization': {
            'Meta': {'object_name': 'Organization'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'people.staff': {
            'Meta': {'object_name': 'Staff'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['people']