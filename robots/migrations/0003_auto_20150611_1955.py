# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0002_auto_20150611_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localcomputer',
            name='group',
            field=models.ManyToManyField(to='auth.Group'),
        ),
    ]
