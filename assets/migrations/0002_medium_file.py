# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.utils


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medium',
            name='file',
            field=models.FileField(null=True, upload_to=common.utils.make_filepath, blank=True),
        ),
    ]
