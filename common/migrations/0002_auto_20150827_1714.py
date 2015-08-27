# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='btbeacon',
            name='x',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='btbeacon',
            name='y',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
