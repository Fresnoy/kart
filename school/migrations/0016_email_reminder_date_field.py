# Generated by Django 4.1 on 2024-10-22 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0015_update_phdstudent'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentapplicationsetup',
            name='application_reminder_email_date',
            field=models.DateField(blank=True, help_text='Email reminder', null=True),
        ),
    ]
