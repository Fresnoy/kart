# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def forwards_func(apps, schema_editor):
    # don't know how to do to keep infos
    pass

def backwards_func(apps, schema_editor):
    # don't know how to do to keep infos
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_studentapp-new_models'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentapplication',
            name='physical_content',
        ),
        migrations.RemoveField(
            model_name='studentapplication',
            name='physical_content_description',
        ),
        migrations.RemoveField(
            model_name='studentapplication',
            name='physical_content_received',
        ),
        migrations.AddField(
            model_name='studentapplication',
            name='binomial_application',
            field=models.BooleanField(default=False, help_text=b'Candidature with another artist'),
        ),
        migrations.AddField(
            model_name='studentapplication',
            name='binomial_application_with',
            field=models.CharField(help_text=b"Name of the binominal artist's candidate with", max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='studentapplication',
            name='campain',
            field=models.ForeignKey(related_name='applications', blank=True, to='school.StudentApplicationSetup', null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='studentapplication',
            name='doctorate_interest',
            field=models.BooleanField(default=False, help_text=b'Interest in the doctorate'),
        ),
        migrations.AddField(
            model_name='studentapplication',
            name='interview_date',
            field=models.DateField(help_text=b'Administration - Date for interview', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='studentapplication',
            name='presentation_video_password',
            field=models.CharField(help_text='Password for the video', max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='studentapplicationsetup',
            name='date_of_birth_max',
            field=models.DateField(help_text=b'Maximum date of birth to apply', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='studentapplicationsetup',
            name='interviews_end_date',
            field=models.DateField(help_text=b'Front : interviews end date', null=True),
        ),
        migrations.AddField(
            model_name='studentapplicationsetup',
            name='interviews_publish_date',
            field=models.DateTimeField(help_text=b'Interviews web publish', null=True),
        ),
        migrations.AddField(
            model_name='studentapplicationsetup',
            name='interviews_start_date',
            field=models.DateField(help_text=b'Front : interviews start date', null=True),
        ),
        migrations.AddField(
            model_name='studentapplicationsetup',
            name='selected_publish_date',
            field=models.DateTimeField(help_text=b'Final selection web publish', null=True),
        ),
        migrations.AlterField(
            model_name='studentapplication',
            name='master_degree',
            field=models.CharField(blank=True, max_length=10, null=True, help_text=b'Obtained a Master Degree', choices=[(b'Y', b'Yes'), (b'N', b'No'), (b'P', b'Pending')]),
        ),
        migrations.RunPython(forwards_func, backwards_func),
        migrations.AlterField(
            model_name='studentapplicationsetup',
            name='candidature_date_end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='studentapplicationsetup',
            name='candidature_date_start',
            field=models.DateTimeField(),
        ),
    ]
