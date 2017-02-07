# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_auto_20170207_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='fresnoyprofile',
            name='homeland_town',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='fresnoyprofile',
            name='residence_town',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
