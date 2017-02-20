# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_studentapplication'),
    ]

    operations = [
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
    ]
