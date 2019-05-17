# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import common.utils


class Migration(migrations.Migration):

    dependencies = [
        ('diffusion', '0002_diffusion'),
        ('production', '0007_task_and_organisation'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='main_event',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='film',
            name='shooting_place',
            field=models.ManyToManyField(to='diffusion.Place', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='ending_date',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.CharField(max_length=10, choices=[(b'FEST', b'Festival'), (b'COMP', b'Competition'), (b'PROJ', b'Projection'), (b'EXHIB', b'Exhibition'), (b'VARN', b'Varnishing'), (b'PARTY', b'Party'), (b'WORKSHOP', b'Workshop'), (b'EVENING', b'Evening')]),
        ),
        migrations.AlterField(
            model_name='film',
            name='genres',
            field=models.ManyToManyField(to='production.FilmGenre', blank=True),
        ),
        migrations.AlterField(
            model_name='production',
            name='picture',
            field=models.ImageField(upload_to=common.utils.make_filepath, blank=True),
        ),
    ]
