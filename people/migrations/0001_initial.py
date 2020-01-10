# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields
from django.conf import settings
import common.utils


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=255, blank=True)),
                ('bio_short_fr', models.TextField(blank=True)),
                ('bio_short_en', models.TextField(blank=True)),
                ('bio_fr', models.TextField(blank=True)),
                ('bio_en', models.TextField(blank=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('twitter_account', models.CharField(max_length=100, blank=True)),
                ('facebook_profile', models.URLField(blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('websites', models.ManyToManyField(to='common.Website', blank=True)),
            ],
            options={
                'ordering': ['user__last_name'],
            },
        ),
        migrations.CreateModel(
            name='FresnoyProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo', models.ImageField(null=True, upload_to=common.utils.make_filepath, blank=True)),
                ('birthdate', models.DateField(null=True, blank=True)),
                ('birthplace', models.CharField(max_length=255, null=True, blank=True)),
                ('birthplace_country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('homeland_address', models.TextField(blank=True)),
                ('homeland_country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('residence_address', models.TextField(blank=True)),
                ('residence_country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('homeland_phone', models.CharField(max_length=50, blank=True)),
                ('residence_phone', models.CharField(max_length=50, blank=True)),
                ('cursus', models.TextField(blank=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('picture', models.ImageField(upload_to=common.utils.make_filepath, blank=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
    ]
