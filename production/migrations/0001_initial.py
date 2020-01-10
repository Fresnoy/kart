# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.utils
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('assets', '0001_initial'),
        ('people', '0001_initial'),
        ('diffusion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('label_fr', models.CharField(max_length=255)),
                ('label_en', models.CharField(max_length=255)),
                ('description_fr', models.TextField()),
                ('description_en', models.TextField()),
                ('gallery', models.ManyToManyField(related_name='itineraries', to='assets.Gallery', blank=True)),
            ],
            options={
                'verbose_name_plural': 'itineraries',
            },
        ),
        migrations.CreateModel(
            name='ItineraryArtwork',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField()),
                ('itinerary', models.ForeignKey(to='production.Itinerary', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='OrganizationTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Production',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(max_length=255, null=True, blank=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('picture', models.ImageField(upload_to=common.utils.make_filepath)),
                ('description_short_fr', models.TextField(null=True, blank=True)),
                ('description_short_en', models.TextField(null=True, blank=True)),
                ('description_fr', models.TextField(null=True, blank=True)),
                ('description_en', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='ProductionOrganizationTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organization', models.ForeignKey(to='people.Organization', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='ProductionStaffTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='StaffTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('production_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='production.Production', on_delete=models.CASCADE)),
                ('production_date', models.DateField()),
                ('credits_fr', models.TextField(null=True, blank=True)),
                ('credits_en', models.TextField(null=True, blank=True)),
                ('thanks_fr', models.TextField(null=True, blank=True)),
                ('thanks_en', models.TextField(null=True, blank=True)),
                ('copyright_fr', models.TextField(null=True, blank=True)),
                ('copyright_en', models.TextField(null=True, blank=True)),
            ],
            bases=('production.production',),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('production_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='production.Production', on_delete=models.CASCADE)),
                ('type', models.CharField(max_length=10, choices=[(b'PROJ', b'Projection'), (b'EXHIB', b'Exhibition'), (b'VARN', b'Varnishing'), (b'PARTY', b'Party'), (b'WORKSHOP', b'Workshop'), (b'EVENING', b'Evening')])),
                ('starting_date', models.DateTimeField()),
                ('ending_date', models.DateTimeField()),
            ],
            bases=('production.production',),
        ),
        migrations.AddField(
            model_name='productionstafftask',
            name='production',
            field=models.ForeignKey(to='production.Production', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='productionstafftask',
            name='staff',
            field=models.ForeignKey(to='people.Staff', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='productionstafftask',
            name='task',
            field=models.ForeignKey(to='production.StaffTask', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='productionorganizationtask',
            name='production',
            field=models.ForeignKey(to='production.Production', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='productionorganizationtask',
            name='task',
            field=models.ForeignKey(to='production.OrganizationTask', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='production',
            name='collaborators',
            field=models.ManyToManyField(related_name='production', through='production.ProductionStaffTask', to='people.Staff', blank=True),
        ),
        migrations.AddField(
            model_name='production',
            name='partners',
            field=models.ManyToManyField(related_name='production', through='production.ProductionOrganizationTask', to='people.Organization', blank=True),
        ),
        migrations.AddField(
            model_name='production',
            name='websites',
            field=models.ManyToManyField(to='common.Website', blank=True),
        ),
        migrations.CreateModel(
            name='Exhibition',
            fields=[
                ('event_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='production.Event', on_delete=models.CASCADE)),
            ],
            bases=('production.event',),
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('artwork_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='production.Artwork', on_delete=models.CASCADE)),
            ],
            bases=('production.artwork',),
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('artwork_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='production.Artwork', on_delete=models.CASCADE)),
                ('technical_description', models.TextField(blank=True)),
            ],
            bases=('production.artwork',),
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('artwork_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='production.Artwork', on_delete=models.CASCADE)),
            ],
            bases=('production.artwork',),
        ),
        migrations.AddField(
            model_name='itineraryartwork',
            name='artwork',
            field=models.ForeignKey(to='production.Artwork', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='itinerary',
            name='artworks',
            field=models.ManyToManyField(to='production.Artwork', through='production.ItineraryArtwork'),
        ),
        migrations.AddField(
            model_name='itinerary',
            name='event',
            field=models.ForeignKey(related_name='itineraries', to='production.Event', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='event',
            name='place',
            field=models.ForeignKey(to='diffusion.Place', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='event',
            name='subevents',
            field=models.ManyToManyField(related_name='subevents_rel_+', to='production.Event', blank=True),
        ),
        migrations.AddField(
            model_name='artwork',
            name='authors',
            field=models.ManyToManyField(related_name='artworks', to='people.Artist'),
        ),
        migrations.AddField(
            model_name='artwork',
            name='beacons',
            field=models.ManyToManyField(related_name='artworks', to='common.BTBeacon', blank=True),
        ),
        migrations.AddField(
            model_name='artwork',
            name='in_situ_galleries',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='artworks_insitu', to='assets.Gallery', blank=True),
        ),
        migrations.AddField(
            model_name='artwork',
            name='mediation_galleries',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='artworks_mediation', to='assets.Gallery', blank=True),
        ),
        migrations.AddField(
            model_name='artwork',
            name='press_galleries',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='artworks_press', to='assets.Gallery', blank=True),
        ),
        migrations.AddField(
            model_name='artwork',
            name='process_galleries',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='artworks_process', to='assets.Gallery', blank=True),
        ),
        migrations.AddField(
            model_name='artwork',
            name='teaser_galleries',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='artworks_teaser', to='assets.Gallery', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='itineraryartwork',
            unique_together=set([('itinerary', 'artwork'), ('itinerary', 'order')]),
        ),
        migrations.AddField(
            model_name='event',
            name='films',
            field=models.ManyToManyField(related_name='events', to='production.Film', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='installations',
            field=models.ManyToManyField(related_name='events', to='production.Installation', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='performances',
            field=models.ManyToManyField(related_name='events', to='production.Performance', blank=True),
        ),
    ]
