from uuid import uuid4
from django.db import models
from django.contrib.auth.models import Group
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from robots import file_provider
import pandas as pd
import django.utils.timezone as tmz
import pytz

import delorean


class SystemModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.CharField(max_length=128, db_index=True)

    class Meta:
        abstract = True


class System(SystemModel):
    group = models.ManyToManyField(Group)
    name = models.CharField(max_length=128)
    timezone = models.CharField(max_length=32)
    shifts = models.ManyToManyField('Shift')


class Shift(SystemModel):
    name = models.CharField(max_length=128)


class LocalComputer(SystemModel):
    group = models.ManyToManyField(Group)
    name = models.CharField(max_length=128)
    registration_token = models.CharField(max_length=128)
    secret_uuid = models.CharField(max_length=128)
    system = models.ForeignKey('System', null=True)
    command_refresh_sec = models.IntegerField(default=10)
    is_running = models.BooleanField(default=False)


COMMAND_NOOP=0
COMMAND_DONE=1
COMMAND_LOAD_PROGRAM=2
COMMAND_STOP_PROGRAM=3

class Command(SystemModel):
    local_computer = models.ForeignKey('LocalComputer')
    type = models.IntegerField(default=COMMAND_NOOP, db_index=True)
    json_command = models.CharField(max_length="512", null=True)
    is_executed = models.BooleanField(default=False, db_index=True)

class Program(SystemModel):
    group = models.ManyToManyField(Group)
    code = models.TextField(null=True)
    description = models.TextField(null=True)
    name = models.CharField(max_length=128)
    sleep_time_sec = models.IntegerField(default=1)

class Map(SystemModel):
    group = models.ManyToManyField(Group)
    name = models.CharField(max_length=128)
    controller = models.ForeignKey('LocalComputer')

ACTUATOR = 1
SENSOR = 2


class MapPoint(SystemModel):
    map = models.ForeignKey('Map')
    point_type = models.IntegerField(default=SENSOR)
    name = models.CharField(max_length=128)
    path = models.CharField(max_length=128)
    controller = models.ForeignKey('LocalComputer')


SIGNAL_PROVIDER = file_provider

class Signal(SystemModel):
    group = models.ManyToManyField(Group)
    name = models.CharField(max_length=128, db_index=True)
    system = models.ForeignKey('System', null=True)
    local_computer = models.ForeignKey('LocalComputer', null=True)

    def add_point(self, value):
        when = tmz.now().astimezone(pytz.UTC)
        millisec = int(delorean.Delorean(when, timezone="UTC").epoch()*1000)
        SIGNAL_PROVIDER.append_data(self.uuid, "[{},{}]".format(value, millisec))

    def get_data(self):
        data = SIGNAL_PROVIDER.get_blob(self.uuid)
        tokens = data.split("]")
        values = [float(token[1:].split(",")[0]) for token in tokens]
        dates = [tmz.datetime.fromtimestamp(token.split(",")[1], tz=pytz.UTC) for token in tokens]
        return values, dates

    def get_time_series(self):
        values, dates = self.get_data()
        return pd.TimeSeries(values, index=dates)

class Setting(SystemModel):
    group = models.ManyToManyField(Group)
    key = models.CharField(max_length=128, db_index=True)
    value = models.CharField(max_length=128)
    local_computer = models.ForeignKey('LocalComputer', null=True)
    system = models.ForeignKey('System', null=True)

    def __unicode__(self):
        return '{},{}'.format(self.key, self.value)

class BinaryBlob(SystemModel):
    group = models.ManyToManyField(Group)
    name = models.CharField(max_length=128, db_index=True)




class SignalBlob(SystemModel):
    signal = models.ForeignKey('Signal')

@receiver(pre_save, sender=Command)
@receiver(pre_save, sender=LocalComputer)
@receiver(pre_save, sender=Map)
@receiver(pre_save, sender=MapPoint)
@receiver(pre_save, sender=Program)
@receiver(pre_save, sender=Shift)
@receiver(pre_save, sender=Signal)
@receiver(pre_save, sender=SignalBlob)
@receiver(pre_save, sender=System)
@receiver(pre_save, sender=Setting)
def set_uuid(sender, instance, **kwargs):
    if not instance.uuid:
        instance.uuid = str(uuid4())
