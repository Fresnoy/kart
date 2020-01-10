# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0005_production_polymorphic_ctype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='aspect_ratio',
            field=models.CharField(blank=True, max_length=10, choices=[(b'1.33', b'1.33 (4/3)'), (b'1.37', b'1.37'), (b'1.66', b'1.66'), (b'1.77', b'1.77 (16/9)'), (b'1.85', b'1.85 (Flat)'), (b'1.90', b'1.90 (Full Container)'), (b'2.39', b'2.39 (Scope)')]),
        ),
    ]
