# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_updatefresnoyprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='fresnoyprofile',
            name='homeland_zipcode',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AddField(
            model_name='fresnoyprofile',
            name='residence_zipcode',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AlterField(
            model_name='fresnoyprofile',
            name='family_status',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
