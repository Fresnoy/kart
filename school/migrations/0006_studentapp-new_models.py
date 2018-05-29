# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.utils


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_studentapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentapplication',
            name='free_document',
            field=models.FileField(help_text=b'Free document', null=True, upload_to=common.utils.make_filepath, blank=True),
        ),
        migrations.AddField(
            model_name='studentapplication',
            name='observation',
            field=models.TextField(help_text=b'Administration - Comments on the application', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='studentapplication',
            name='reference_letter',
            field=models.FileField(help_text=b'Reference / Recommendation letter', null=True, upload_to=common.utils.make_filepath, blank=True),
        ),
        migrations.AddField(
            model_name='studentapplication',
            name='unselected',
            field=models.BooleanField(default=False, help_text=b'Administration - Is the candidat not choosen by the Jury'),
        ),
        migrations.AddField(
            model_name='studentapplication',
            name='wait_listed_for_interview',
            field=models.BooleanField(default=False, help_text=b'Administration - Is the candidat wait listed for the Interview'),
        ),
    ]
