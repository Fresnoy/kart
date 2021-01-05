# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0002_auto_20150610_1203'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilmGenre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='InstallationGenre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='film',
            name='aspect_ratio',
            field=models.CharField(blank=True, max_length=10, choices=[(b'1.33', b'1.33'), (b'1.37', b'1.37'), (b'1.66', b'1.66'), (b'1.77', b'1.77'), (b'1.85', b'1.85'), (b'1.89', b'1.89'), (b'2.35', b'2.35'), (b'4/3', b'4/3'), (b'16/9', b'16/9')]),
        ),
        migrations.AlterField(
            model_name='film',
            name='duration',
            field=models.DurationField(help_text=b'Sous la forme HH:MM:SS', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='film',
            name='genres',
            field=models.ManyToManyField(to='production.FilmGenre'),
        ),
        migrations.AddField(
            model_name='installation',
            name='genres',
            field=models.ManyToManyField(to='production.InstallationGenre'),
        ),
    ]
