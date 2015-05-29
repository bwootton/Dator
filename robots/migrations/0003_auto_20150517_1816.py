# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('robots', '0002_robot_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Controller',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.CharField(max_length=128, db_index=True)),
                ('name', models.CharField(max_length=128)),
                ('group', models.ForeignKey(to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.CharField(max_length=128, db_index=True)),
                ('name', models.CharField(max_length=128)),
                ('controller', models.ForeignKey(to='robots.Controller')),
                ('group', models.ForeignKey(to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='MapPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.CharField(max_length=128, db_index=True)),
                ('point_type', models.IntegerField(default=2)),
                ('name', models.CharField(max_length=128)),
                ('path', models.CharField(max_length=128)),
                ('controller', models.ForeignKey(to='robots.Controller')),
                ('map', models.ForeignKey(to='robots.Map')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.CharField(max_length=128, db_index=True)),
                ('code', models.TextField()),
                ('description', models.TextField(null=True)),
                ('name', models.CharField(max_length=128)),
                ('group', models.ForeignKey(to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.CharField(max_length=128, db_index=True)),
                ('name', models.CharField(max_length=128)),
                ('group', models.ForeignKey(to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Signal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.CharField(max_length=128, db_index=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='SignalBlob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.CharField(max_length=128, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uuid', models.CharField(max_length=128, db_index=True)),
                ('name', models.CharField(max_length=128)),
                ('timezone', models.CharField(max_length=32)),
                ('group', models.ForeignKey(to='auth.Group')),
                ('shifts', models.ManyToManyField(to='robots.Shift')),
            ],
        ),
        migrations.RemoveField(
            model_name='robot',
            name='group',
        ),
        migrations.DeleteModel(
            name='robot',
        ),
        migrations.AddField(
            model_name='signal',
            name='blobs',
            field=models.ManyToManyField(to='robots.SignalBlob'),
        ),
        migrations.AddField(
            model_name='signal',
            name='group',
            field=models.ForeignKey(to='auth.Group'),
        ),
        migrations.AddField(
            model_name='controller',
            name='system',
            field=models.ForeignKey(to='robots.System'),
        ),
    ]
