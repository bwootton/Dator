# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_api', '0020_experiment_media_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='media_link',
        ),
    ]
