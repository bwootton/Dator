# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('robots', '0003_auto_20150517_1816'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shift',
            name='group',
        ),
        migrations.RemoveField(
            model_name='signal',
            name='blobs',
        ),
        migrations.AddField(
            model_name='signalblob',
            name='signal',
            field=models.ForeignKey(default=0, to='robots.Signal'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='controller',
            name='group',
        ),
        migrations.AddField(
            model_name='controller',
            name='group',
            field=models.ManyToManyField(to='auth.Group'),
        ),
        migrations.RemoveField(
            model_name='map',
            name='group',
        ),
        migrations.AddField(
            model_name='map',
            name='group',
            field=models.ManyToManyField(to='auth.Group'),
        ),
        migrations.RemoveField(
            model_name='program',
            name='group',
        ),
        migrations.AddField(
            model_name='program',
            name='group',
            field=models.ManyToManyField(to='auth.Group'),
        ),
        migrations.RemoveField(
            model_name='signal',
            name='group',
        ),
        migrations.AddField(
            model_name='signal',
            name='group',
            field=models.ManyToManyField(to='auth.Group'),
        ),
        migrations.RemoveField(
            model_name='system',
            name='group',
        ),
        migrations.AddField(
            model_name='system',
            name='group',
            field=models.ManyToManyField(to='auth.Group'),
        ),
    ]
