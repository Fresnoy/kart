# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_updatefresnoyprofile'),
        ('assets', '0001_initial'),
        ('school', '0004_rename_newstudent_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_year_application_count', models.CharField(default=None, help_text='Auto generated field (current year - increment number)', max_length=8, blank=True)),
                ('first_time', models.BooleanField(default=True, help_text=b"If the first time the Artist's applying")),
                ('last_application_year', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('remote_interview', models.BooleanField(default=False)),
                ('remote_interview_type', models.CharField(help_text='Skype / Gtalk / FaceTime / AppearIn / Other', max_length=50, blank=True)),
                ('remote_interview_info', models.CharField(help_text=b'ID / Number / ... ', max_length=50, blank=True)),
                ('asynchronous_element', models.BooleanField(default=False, help_text=b'Element not sent by current form')),
                ('asynchronous_element_description', models.TextField(help_text=b'What are these elements and how you send it', null=True, blank=True)),
                ('asynchronous_element_received', models.BooleanField(default=False, help_text=b'Administration - Element have been received')),
                ('remark', models.TextField(help_text=b"Free expression'", null=True, blank=True)),
                ('application_completed', models.BooleanField(default=False, help_text=b"Candidature's validation")),
                ('selected_for_interview', models.BooleanField(default=False, help_text=b'Administration - Is the candidat selected for the Interview')),
                ('selected_for_petit_jury', models.BooleanField(default=False, help_text=b"Administration - Is the candidat selected for the 'Petit Jury'")),
                ('selected_for_grand_jury', models.BooleanField(default=False, help_text=b"Administration - Is the candidat selected for the 'Grand Jury'")),
                ('application_complete', models.BooleanField(default=False, help_text=b'Administration - Candidature is complete')),
                ('administrative_galleries', sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='student_application_administrative', to='assets.Gallery', blank=True)),
                ('artist', models.ForeignKey(related_name='student_application', to='people.Artist')),
                ('artwork_galleries', sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='student_application_artwork', to='assets.Gallery', blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='student',
            name='artist',
            field=models.OneToOneField(related_name='student', to='people.Artist'),
        ),
    ]
