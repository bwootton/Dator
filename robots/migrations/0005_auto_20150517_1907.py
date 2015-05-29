# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0004_auto_20150517_1857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controller',
            name='group',
        ),
        migrations.RemoveField(
            model_name='controller',
            name='system',
        ),
        migrations.RemoveField(
            model_name='map',
            name='controller',
        ),
        migrations.RemoveField(
            model_name='map',
            name='group',
        ),
        migrations.RemoveField(
            model_name='mappoint',
            name='controller',
        ),
        migrations.RemoveField(
            model_name='mappoint',
            name='map',
        ),
        migrations.RemoveField(
            model_name='program',
            name='group',
        ),
        migrations.RemoveField(
            model_name='signal',
            name='group',
        ),
        migrations.RemoveField(
            model_name='signalblob',
            name='signal',
        ),
        migrations.RemoveField(
            model_name='system',
            name='group',
        ),
        migrations.RemoveField(
            model_name='system',
            name='shifts',
        ),
        migrations.DeleteModel(
            name='Controller',
        ),
        migrations.DeleteModel(
            name='Map',
        ),
        migrations.DeleteModel(
            name='MapPoint',
        ),
        migrations.DeleteModel(
            name='Program',
        ),
        migrations.DeleteModel(
            name='Shift',
        ),
        migrations.DeleteModel(
            name='Signal',
        ),
        migrations.DeleteModel(
            name='SignalBlob',
        ),
        migrations.DeleteModel(
            name='System',
        ),
    ]
