# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_updatefresnoyprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('production', '0007_task_and_organisation'),
        ('diffusion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diffusion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(null=True)),
                ('amount', models.CharField(help_text=b'money, visibility, currency free', max_length=255, blank=True)),
                ('note', models.TextField(help_text=b'Free note', blank=True)),
                ('artwork', models.ForeignKey(related_name='rewards', to='production.Artwork')),
            ],
        ),
        migrations.AddField(
            model_name='award',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='award',
            name='event',
            field=models.ForeignKey(related_name='award', to='production.Event', help_text=b'Main Event', null=True),
        ),
        migrations.AddField(
            model_name='award',
            name='label',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='award',
            name='task',
            field=models.ForeignKey(related_name='award', blank=True, to='production.StaffTask', null=True),
        ),
        migrations.AddField(
            model_name='award',
            name='type',
            field=models.CharField(max_length=10, null=True, choices=[(b'ARTWORK', b'Artwork'), (b'ARTIST', b'Artist')]),
        ),
        migrations.AddField(
            model_name='place',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='place',
            name='country',
            field=django_countries.fields.CountryField(default=b'', max_length=2),
        ),
        migrations.AddField(
            model_name='place',
            name='latitude',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True),
        ),
        migrations.AddField(
            model_name='place',
            name='longitude',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=6, blank=True),
        ),
        migrations.AddField(
            model_name='place',
            name='town',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='place',
            name='zipcode',
            field=models.CharField(help_text=b'Code postal / Zipcode', max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='organization',
            field=models.ForeignKey(related_name='places', blank=True, to='people.Organization', null=True),
        ),
        migrations.AddField(
            model_name='reward',
            name='award',
            field=models.ForeignKey(related_name='reward', to='diffusion.Award'),
        ),
        migrations.AddField(
            model_name='reward',
            name='event',
            field=models.ForeignKey(related_name='reward', to='production.Event'),
        ),
        migrations.AddField(
            model_name='reward',
            name='giver',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text=b'Who hands the prize', null=True),
        ),
        migrations.AddField(
            model_name='reward',
            name='sponsor',
            field=models.ForeignKey(related_name='reward', blank=True, to='people.Organization', null=True),
        ),
    ]
