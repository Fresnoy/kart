# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('starting_year', models.PositiveSmallIntegerField()),
                ('ending_year', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ['starting_year'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('artist_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='people.Artist', on_delete=models.CASCADE)),
                ('number', models.CharField(max_length=50, null=True, blank=True)),
                ('promotion', models.ForeignKey(related_name='students', to='school.Promotion', on_delete=models.CASCADE)),
            ],
            bases=('people.artist',),
        ),
    ]
