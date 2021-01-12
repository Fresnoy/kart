# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0005_production_polymorphic_ctype'),
        ('school', '0003_newstudent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='artist_ptr',
        ),
        migrations.RemoveField(
            model_name='student',
            name='promotion',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.RenameModel(
            old_name='NewStudent',
            new_name='Student'
        )
    ]
