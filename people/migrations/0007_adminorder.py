# Generated by Django 4.1 on 2023-10-18 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0006_languagesfield_newversion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fresnoyprofile',
            options={'ordering': ['user__first_name']},
        ),
    ]
