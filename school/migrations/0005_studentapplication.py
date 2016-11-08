# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
        ('people', '0002_updatefresnoyprofile'),
        ('people', '0001_initial'),
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
                ('selected_for_interview', models.BooleanField(default=False, help_text=b'Is the candidat selected for the Interview')),
                ('administrative_galleries', sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='certificates', to='assets.Gallery', blank=True)),
                ('artist', models.ForeignKey(related_name='student_application', to='people.Artist')),
                ('artwork_galleries', sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='artworks', to='assets.Gallery', blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='student',
            name='artist',
            field=models.OneToOneField(related_name='student', to='people.Artist'),
        ),
    ]
