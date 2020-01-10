# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def forwards_func(apps, schema_editor):
    ProductionModel = apps.get_model('production', 'Production')
    FilmModel = apps.get_model('production', 'Film')
    InstallationModel = apps.get_model('production', 'Installation')
    PerformanceModel = apps.get_model('production', 'Performance')
    EventModel = apps.get_model('production', 'Event')

    models = [FilmModel, InstallationModel, PerformanceModel, EventModel]

    ContentType = apps.get_model('contenttypes', 'ContentType')
    for model in models:
        new_ct = ContentType.objects.get_for_model(model)
        model.objects.filter(polymorphic_ctype__isnull=True).update(polymorphic_ctype=new_ct)

def backwards_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('production', '0004_production_former_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='production',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_production.production_set+', editable=False, to='contenttypes.ContentType', null=True, on_delete=models.CASCADE),
        ),
        migrations.RunPython(forwards_func, backwards_func)
    ]
