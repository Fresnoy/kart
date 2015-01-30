# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ProductionOrganizationTask.task'
        db.alter_column(u'production_productionorganizationtask', 'task_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['production.OrganizationTask']))

    def backwards(self, orm):

        # Changing field 'ProductionOrganizationTask.task'
        db.alter_column(u'production_productionorganizationtask', 'task_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['production.StaffTask']))

    models = {
        u'assets.gallery': {
            'Meta': {'object_name': 'Gallery'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
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
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'diffusion.place': {
            'Meta': {'object_name': 'Place'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'places'", 'to': u"orm['people.Organization']"})
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
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'websites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Website']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'people.organization': {
            'Meta': {'object_name': 'Organization'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'people.staff': {
            'Meta': {'object_name': 'Staff'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'production.artwork': {
            'Meta': {'object_name': 'Artwork', '_ormbases': [u'production.Production']},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'artworks'", 'symmetrical': 'False', 'to': u"orm['people.Artist']"}),
            'beacons': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'artworks'", 'blank': 'True', 'to': u"orm['common.BTBeacon']"}),
            'copyright_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'copyright_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'credits_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'credits_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'in_situ_galleries': ('sortedm2m.fields.SortedManyToManyField', [], {'symmetrical': 'False', 'related_name': "'artworks_insitu'", 'blank': 'True', 'to': u"orm['assets.Gallery']"}),
            'mediation_galleries': ('sortedm2m.fields.SortedManyToManyField', [], {'symmetrical': 'False', 'related_name': "'artworks_mediation'", 'blank': 'True', 'to': u"orm['assets.Gallery']"}),
            'process_galleries': ('sortedm2m.fields.SortedManyToManyField', [], {'symmetrical': 'False', 'related_name': "'artworks_process'", 'blank': 'True', 'to': u"orm['assets.Gallery']"}),
            'production_date': ('django.db.models.fields.DateField', [], {}),
            u'production_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['production.Production']", 'unique': 'True', 'primary_key': 'True'}),
            'thanks_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'thanks_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'production.event': {
            'Meta': {'object_name': 'Event', '_ormbases': [u'production.Production']},
            'ending_date': ('django.db.models.fields.DateTimeField', [], {}),
            'films': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'events'", 'blank': 'True', 'to': u"orm['production.Film']"}),
            'installations': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'events'", 'blank': 'True', 'to': u"orm['production.Installation']"}),
            'performances': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'events'", 'blank': 'True', 'to': u"orm['production.Performance']"}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['diffusion.Place']"}),
            u'production_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['production.Production']", 'unique': 'True', 'primary_key': 'True'}),
            'starting_date': ('django.db.models.fields.DateTimeField', [], {}),
            'subevents': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'subevents_rel_+'", 'blank': 'True', 'to': u"orm['production.Event']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'production.exhibition': {
            'Meta': {'object_name': 'Exhibition', '_ormbases': [u'production.Event']},
            u'event_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['production.Event']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'production.film': {
            'Meta': {'object_name': 'Film', '_ormbases': [u'production.Artwork']},
            u'artwork_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['production.Artwork']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'production.installation': {
            'Meta': {'object_name': 'Installation', '_ormbases': [u'production.Artwork']},
            u'artwork_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['production.Artwork']", 'unique': 'True', 'primary_key': 'True'}),
            'technical_description': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'production.itinerary': {
            'Meta': {'object_name': 'Itinerary'},
            'artworks': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['production.Artwork']", 'through': u"orm['production.ItineraryArtwork']", 'symmetrical': 'False'}),
            'description_en': ('django.db.models.fields.TextField', [], {}),
            'description_fr': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'itineraries'", 'to': u"orm['production.Event']"}),
            'gallery': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'itineraries'", 'blank': 'True', 'to': u"orm['assets.Gallery']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'label_fr': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'production.itineraryartwork': {
            'Meta': {'ordering': "('order',)", 'unique_together': "(('itinerary', 'artwork'), ('itinerary', 'order'))", 'object_name': 'ItineraryArtwork'},
            'artwork': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['production.Artwork']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itinerary': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['production.Itinerary']"}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'production.organizationtask': {
            'Meta': {'object_name': 'OrganizationTask'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'production.performance': {
            'Meta': {'object_name': 'Performance', '_ormbases': [u'production.Artwork']},
            u'artwork_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['production.Artwork']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'production.production': {
            'Meta': {'object_name': 'Production'},
            'collaborators': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'production'", 'blank': 'True', 'through': u"orm['production.ProductionStaffTask']", 'to': u"orm['people.Staff']"}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_short_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_short_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'partners': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'production'", 'blank': 'True', 'through': u"orm['production.ProductionOrganizationTask']", 'to': u"orm['people.Organization']"}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'websites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Website']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'production.productionorganizationtask': {
            'Meta': {'object_name': 'ProductionOrganizationTask'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Organization']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['production.Production']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['production.OrganizationTask']"})
        },
        u'production.productionstafftask': {
            'Meta': {'object_name': 'ProductionStaffTask'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['production.Production']"}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Staff']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['production.StaffTask']"})
        },
        u'production.stafftask': {
            'Meta': {'object_name': 'StaffTask'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['production']