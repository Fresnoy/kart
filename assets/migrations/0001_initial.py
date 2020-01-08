# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.utils


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'galleries',
            },
        ),
        migrations.CreateModel(
            name='Medium',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('position', models.PositiveIntegerField(default=1)),
                ('label', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('picture', models.ImageField(null=True, upload_to=common.utils.make_filepath, blank=True)),
                ('medium_url', models.URLField(null=True, blank=True)),
                ('gallery', models.ForeignKey(related_name='media', to='assets.Gallery', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('position',),
                'verbose_name_plural': 'media',
            },
        ),
    ]
