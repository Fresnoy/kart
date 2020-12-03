# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

def forwards_func(apps, schema_editor):
    NewStudent = apps.get_model('school', 'NewStudent')
    Student = apps.get_model('school', 'Student')

    if Student.objects.all().count()>0:
        for student in Student.objects.all():
            ns = NewStudent()
            ns.number = student.number
            ns.promotion = student.promotion
            ns.graduate = student.graduate
            ns.user = student.user
            ns.artist_id = student.artist_ptr_id
            ns.save()

def backwards_func(apps, schema_editor):
    pass



class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0002_student_graduate'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewStudent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=50, null=True, blank=True)),
                ('graduate', models.BooleanField(default=False)),
                ('artist', models.OneToOneField(to='people.Artist', on_delete=models.CASCADE)),
                ('promotion', models.ForeignKey(to='school.Promotion', on_delete=models.CASCADE)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.RunPython(forwards_func, backwards_func)
    ]
