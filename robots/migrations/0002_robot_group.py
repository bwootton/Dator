# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('robots', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='robot',
            name='group',
            field=models.ForeignKey(default=0, to='auth.Group'),
            preserve_default=False,
        ),
    ]
