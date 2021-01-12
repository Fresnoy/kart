# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='aspect_ratio',
            field=models.CharField(blank=True, max_length=10, choices=[(b'1.33', b'1.33'), (b'1.37', b'1.37'), (b'1.66', b'1.66'), (b'1.77', b'1.77'), (b'1.85', b'1.85'), (b'1.89', b'1.89'), (b'2.35', b'2.35'), (b'4/3', b'4/3')]),
        ),
        migrations.AddField(
            model_name='film',
            name='duration',
            field=models.DurationField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='film',
            name='process',
            field=models.CharField(blank=True, max_length=10, choices=[(b'COLOR', b'Couleur'), (b'BW', b'Noir & Blanc'), (b'COLORBW', b'NB & Couleur'), (b'SEPIA', b'S\xc3\xa9pia')]),
        ),
        migrations.AddField(
            model_name='film',
            name='shooting_format',
            field=models.CharField(blank=True, max_length=10, choices=[(b'SUP8', b'Super 8'), (b'SUP16', b'Super 16'), (b'SUP35', b'Super 35'), (b'35MM', b'35 MM'), (b'70MM', b'70 MM'), (b'DV', b'DV'), (b'DVCAM', b'DV-CAM'), (b'HD', b'HD'), (b'HDCAM', b'HD-CAM'), (b'HDCINE', b'HD CINEMASCOPE'), (b'CREANUM', b'CREATION NUMERIQUE'), (b'BETASP', b'BETA SP'), (b'BETANUM', b'BETA NUM.'), (b'DIGICAM', b'APPAREIL PHOTO'), (b'MOBILE', b'MOBILE'), (b'HI8', b'HI8'), (b'AVCHD', b'AVCHD'), (b'XDCAMEX', b'XDcamEX'), (b'3DREL', b'RELIEF 3D'), (b'2K', b'2K'), (b'4K', b'4K')]),
        ),
    ]
