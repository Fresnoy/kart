# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0003_auto_20150610_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='production',
            name='former_title',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
