# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StaffTask'
        db.create_table(u'production_stafftask', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'production', ['StaffTask'])

        # Adding model 'OrganizationTask'
        db.create_table(u'production_organizationtask', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'production', ['OrganizationTask'])

        # Adding model 'ProductionStaffTask'
        db.create_table(u'production_productionstafftask', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('staff', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Staff'])),
            ('production', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['production.Production'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['production.StaffTask'])),
        ))
        db.send_create_signal(u'production', ['ProductionStaffTask'])

        # Adding model 'ProductionOrganizationTask'
        db.create_table(u'production_productionorganizationtask', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Organization'])),
            ('production', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['production.Production'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['production.StaffTask'])),
        ))
        db.send_create_signal(u'production', ['ProductionOrganizationTask'])

        # Adding model 'Production'
        db.create_table(u'production_production', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('description_short_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_short_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'production', ['Production'])

        # Adding M2M table for field websites on 'Production'
        m2m_table_name = db.shorten_name(u'production_production_websites')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('production', models.ForeignKey(orm[u'production.production'], null=False)),
            ('website', models.ForeignKey(orm[u'common.website'], null=False))
        ))
        db.create_unique(m2m_table_name, ['production_id', 'website_id'])

        # Adding model 'Artwork'
        db.create_table(u'production_artwork', (
            (u'production_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['production.Production'], unique=True, primary_key=True)),
            ('production_date', self.gf('django.db.models.fields.DateField')()),
            ('credits_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('credits_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('thanks_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('thanks_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('copyright_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('copyright_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'production', ['Artwork'])

        # Adding M2M table for field process_galleries on 'Artwork'
        m2m_table_name = db.shorten_name(u'production_artwork_process_galleries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artwork', models.ForeignKey(orm[u'production.artwork'], null=False)),
            ('gallery', models.ForeignKey(orm[u'assets.gallery'], null=False))
        ))
        db.create_unique(m2m_table_name, ['artwork_id', 'gallery_id'])

        # Adding M2M table for field mediation_galleries on 'Artwork'
        m2m_table_name = db.shorten_name(u'production_artwork_mediation_galleries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artwork', models.ForeignKey(orm[u'production.artwork'], null=False)),
            ('gallery', models.ForeignKey(orm[u'assets.gallery'], null=False))
        ))
        db.create_unique(m2m_table_name, ['artwork_id', 'gallery_id'])

        # Adding M2M table for field in_situ_galleries on 'Artwork'
        m2m_table_name = db.shorten_name(u'production_artwork_in_situ_galleries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artwork', models.ForeignKey(orm[u'production.artwork'], null=False)),
            ('gallery', models.ForeignKey(orm[u'assets.gallery'], null=False))
        ))
        db.create_unique(m2m_table_name, ['artwork_id', 'gallery_id'])

        # Adding M2M table for field authors on 'Artwork'
        m2m_table_name = db.shorten_name(u'production_artwork_authors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artwork', models.ForeignKey(orm[u'production.artwork'], null=False)),
            ('artist', models.ForeignKey(orm[u'people.artist'], null=False))
        ))
        db.create_unique(m2m_table_name, ['artwork_id', 'artist_id'])

        # Adding model 'Film'
        db.create_table(u'production_film', (
            (u'artwork_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['production.Artwork'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'production', ['Film'])

        # Adding model 'Installation'
        db.create_table(u'production_installation', (
            (u'artwork_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['production.Artwork'], unique=True, primary_key=True)),
            ('technical_description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'production', ['Installation'])

        # Adding model 'Performance'
        db.create_table(u'production_performance', (
            (u'artwork_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['production.Artwork'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'production', ['Performance'])

        # Adding model 'Event'
        db.create_table(u'production_event', (
            (u'production_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['production.Production'], unique=True, primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('starting_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('ending_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['diffusion.Place'])),
        ))
        db.send_create_signal(u'production', ['Event'])

        # Adding M2M table for field installations on 'Event'
        m2m_table_name = db.shorten_name(u'production_event_installations')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'production.event'], null=False)),
            ('installation', models.ForeignKey(orm[u'production.installation'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'installation_id'])

        # Adding M2M table for field films on 'Event'
        m2m_table_name = db.shorten_name(u'production_event_films')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'production.event'], null=False)),
            ('film', models.ForeignKey(orm[u'production.film'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'film_id'])

        # Adding M2M table for field performances on 'Event'
        m2m_table_name = db.shorten_name(u'production_event_performances')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'production.event'], null=False)),
            ('performance', models.ForeignKey(orm[u'production.performance'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'performance_id'])

        # Adding M2M table for field subevents on 'Event'
        m2m_table_name = db.shorten_name(u'production_event_subevents')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_event', models.ForeignKey(orm[u'production.event'], null=False)),
            ('to_event', models.ForeignKey(orm[u'production.event'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_event_id', 'to_event_id'])

        # Adding model 'Exhibition'
        db.create_table(u'production_exhibition', (
            (u'event_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['production.Event'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'production', ['Exhibition'])

        # Adding model 'Itinerary'
        db.create_table(u'production_itinerary', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label_fr', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('label_en', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description_fr', self.gf('django.db.models.fields.TextField')()),
            ('description_en', self.gf('django.db.models.fields.TextField')()),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='itineraries', to=orm['production.Event'])),
        ))
        db.send_create_signal(u'production', ['Itinerary'])

        # Adding model 'ItineraryArtwork'
        db.create_table(u'production_itineraryartwork', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('itinerary', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['production.Itinerary'])),
            ('artwork', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['production.Artwork'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'production', ['ItineraryArtwork'])

        # Adding unique constraint on 'ItineraryArtwork', fields ['itinerary', 'artwork']
        db.create_unique(u'production_itineraryartwork', ['itinerary_id', 'artwork_id'])

        # Adding unique constraint on 'ItineraryArtwork', fields ['itinerary', 'order']
        db.create_unique(u'production_itineraryartwork', ['itinerary_id', 'order'])


    def backwards(self, orm):
        # Removing unique constraint on 'ItineraryArtwork', fields ['itinerary', 'order']
        db.delete_unique(u'production_itineraryartwork', ['itinerary_id', 'order'])

        # Removing unique constraint on 'ItineraryArtwork', fields ['itinerary', 'artwork']
        db.delete_unique(u'production_itineraryartwork', ['itinerary_id', 'artwork_id'])

        # Deleting model 'StaffTask'
        db.delete_table(u'production_stafftask')

        # Deleting model 'OrganizationTask'
        db.delete_table(u'production_organizationtask')

        # Deleting model 'ProductionStaffTask'
        db.delete_table(u'production_productionstafftask')

        # Deleting model 'ProductionOrganizationTask'
        db.delete_table(u'production_productionorganizationtask')

        # Deleting model 'Production'
        db.delete_table(u'production_production')

        # Removing M2M table for field websites on 'Production'
        db.delete_table(db.shorten_name(u'production_production_websites'))

        # Deleting model 'Artwork'
        db.delete_table(u'production_artwork')

        # Removing M2M table for field process_galleries on 'Artwork'
        db.delete_table(db.shorten_name(u'production_artwork_process_galleries'))

        # Removing M2M table for field mediation_galleries on 'Artwork'
        db.delete_table(db.shorten_name(u'production_artwork_mediation_galleries'))

        # Removing M2M table for field in_situ_galleries on 'Artwork'
        db.delete_table(db.shorten_name(u'production_artwork_in_situ_galleries'))

        # Removing M2M table for field authors on 'Artwork'
        db.delete_table(db.shorten_name(u'production_artwork_authors'))

        # Deleting model 'Film'
        db.delete_table(u'production_film')

        # Deleting model 'Installation'
        db.delete_table(u'production_installation')

        # Deleting model 'Performance'
        db.delete_table(u'production_performance')

        # Deleting model 'Event'
        db.delete_table(u'production_event')

        # Removing M2M table for field installations on 'Event'
        db.delete_table(db.shorten_name(u'production_event_installations'))

        # Removing M2M table for field films on 'Event'
        db.delete_table(db.shorten_name(u'production_event_films'))

        # Removing M2M table for field performances on 'Event'
        db.delete_table(db.shorten_name(u'production_event_performances'))

        # Removing M2M table for field subevents on 'Event'
        db.delete_table(db.shorten_name(u'production_event_subevents'))

        # Deleting model 'Exhibition'
        db.delete_table(u'production_exhibition')

        # Deleting model 'Itinerary'
        db.delete_table(u'production_itinerary')

        # Deleting model 'ItineraryArtwork'
        db.delete_table(u'production_itineraryartwork')


    models = {
        u'assets.gallery': {
            'Meta': {'object_name': 'Gallery'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'websites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Website']", 'symmetrical': 'False', 'blank': 'True'})
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
        },
        u'production.artwork': {
            'Meta': {'object_name': 'Artwork', '_ormbases': [u'production.Production']},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'artwork'", 'symmetrical': 'False', 'to': u"orm['people.Artist']"}),
            'copyright_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'copyright_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'credits_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'credits_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'in_situ_galleries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'artworks_insitu'", 'blank': 'True', 'to': u"orm['assets.Gallery']"}),
            'mediation_galleries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'artworks_mediation'", 'blank': 'True', 'to': u"orm['assets.Gallery']"}),
            'process_galleries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'artworks_process'", 'blank': 'True', 'to': u"orm['assets.Gallery']"}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'label_fr': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'websites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['common.Website']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'production.productionorganizationtask': {
            'Meta': {'object_name': 'ProductionOrganizationTask'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['people.Organization']"}),
            'production': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['production.Production']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['production.StaffTask']"})
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