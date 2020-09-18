# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0007_studentapp-models-v3'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentapplication',
            old_name='campain',
            new_name='campaign',
        ),
        migrations.AlterField(
            model_name='studentapplication',
            name='interview_date',
            field=models.DateTimeField(help_text=b'Administration - Date for interview', null=True, blank=True),
        ),
    ]
