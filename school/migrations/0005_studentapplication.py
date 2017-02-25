# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import common.utils


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_updatefresnoyprofile'),
        ('assets', '0002_medium_file'),
        ('school', '0004_rename_newstudent_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentApplication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_year_application_count', models.CharField(default=None, help_text='Auto generated field (current year - increment number)', max_length=8, blank=True)),
                ('identity_card', models.FileField(help_text=b'Identity justificative', null=True, upload_to=common.utils.make_filepath, blank=True)),
                ('first_time', models.BooleanField(default=False, help_text=b"If the first time the Artist's applying")),
                ('last_applications_years', models.CharField(help_text='Already candidate', max_length=50, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('remote_interview', models.BooleanField(default=False)),
                ('remote_interview_type', models.CharField(help_text='Skype / Gtalk / FaceTime / AppearIn / Other', max_length=50, blank=True)),
                ('remote_interview_info', models.CharField(help_text=b'ID / Number / ... ', max_length=50, blank=True)),
                ('master_degree', models.NullBooleanField(default=None, help_text=b'Obtained a Master  Degree')),
                ('experience_justification', models.FileField(help_text=b'If no master Degree, experience letter', null=True, upload_to=common.utils.make_filepath, blank=True)),
                ('curriculum_vitae', models.FileField(help_text=b'BIO CV', null=True, upload_to=common.utils.make_filepath, blank=True)),
                ('justification_letter', models.FileField(help_text=b'Justification / Motivation', null=True, upload_to=common.utils.make_filepath, blank=True)),
                ('considered_project_1', models.FileField(help_text=b'Considered project first year', null=True, upload_to=common.utils.make_filepath, blank=True)),
                ('artistic_referencies_project_1', models.TextField(help_text=b"Artistic references for the first year's project", null=True, blank=True)),
                ('considered_project_2', models.FileField(help_text=b'Considered project second year', null=True, upload_to=common.utils.make_filepath, blank=True)),
                ('artistic_referencies_project_2', models.TextField(help_text=b"Artistic references for second first year's project", null=True, blank=True)),
                ('presentation_video', models.URLField(help_text=b'Url presentation video Link', null=True, blank=True)),
                ('presentation_video_details', models.TextField(help_text=b'Details for the video', null=True, blank=True)),
                ('physical_content', models.BooleanField(default=False, help_text=b'Element not sent by current form')),
                ('physical_content_description', models.TextField(help_text=b'What are these elements and how you send it', null=True, blank=True)),
                ('physical_content_received', models.BooleanField(default=False, help_text=b'Administration - Element have been received')),
                ('remark', models.TextField(help_text=b"Free expression'", null=True, blank=True)),
                ('application_completed', models.BooleanField(default=False, help_text=b"Candidature's validation")),
                ('selected_for_interview', models.BooleanField(default=False, help_text=b'Administration - Is the candidat selected for the Interview')),
                ('selected', models.BooleanField(default=False, help_text=b'Administration - Is the candidat selected')),
                ('wait_listed', models.BooleanField(default=False, help_text=b'Administration - Is the candidat wait listed')),
                ('application_complete', models.BooleanField(default=False, help_text=b'Administration - Candidature is complete')),
                ('artist', models.ForeignKey(related_name='student_application', to='people.Artist')),
                ('cursus_justifications', models.ForeignKey(related_name='student_application_cursus_justification', blank=True, to='assets.Gallery', help_text=b'Gallery of justificaitons', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentApplicationSetup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25, null=True, blank=True)),
                ('candidature_date_start', models.DateField()),
                ('candidature_date_end', models.DateField()),
                ('candidatures_url', models.URLField(help_text=b'Front : Url list of candidatures')),
                ('reset_password_url', models.URLField(help_text=b'Front : Url reset password')),
                ('recover_password_url', models.URLField(help_text=b'Front : Url recover password')),
                ('authentification_url', models.URLField(help_text=b'Front : Url authentification')),
                ('video_service_name', models.CharField(help_text=b'video service name', max_length=25, null=True, blank=True)),
                ('video_service_url', models.URLField(help_text=b'service URL')),
                ('video_service_token', models.CharField(help_text=b'Video service token', max_length=128, null=True, blank=True)),
                ('is_current_setup', models.BooleanField(default=True, help_text=b'This configuration is actived')),
                ('promotion', models.ForeignKey(to='school.Promotion')),
            ],
        ),
        migrations.AlterField(
            model_name='student',
            name='artist',
            field=models.OneToOneField(related_name='student', to='people.Artist'),
        ),
    ]
