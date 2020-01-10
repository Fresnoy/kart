# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BTBeacon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('uuid', models.UUIDField(unique=True, max_length=32)),
                ('rssi_in', models.IntegerField()),
                ('rssi_out', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title_fr', models.CharField(max_length=255)),
                ('title_en', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=2, choices=[(b'FR', b'French'), (b'EN', b'English')])),
                ('url', models.URLField()),
            ],
        ),
    ]
