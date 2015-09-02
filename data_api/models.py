from uuid import uuid4
from django.db import models
from django.contrib.auth.models import Group
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from data_api import file_provider
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


class Event(SystemModel):
    """
    An event is used to record controller specific events for correlation with data signals.
    """
    group = models.ManyToManyField(Group)
    type = models.CharField(max_length=32)
    info = models.TextField(null=True)
    local_computer = models.ForeignKey('LocalComputer', null=True)
    system = models.ForeignKey('System', null=True)


class System(SystemModel):
    """
    A system is a group of related LocalComputers that  coordinate actions and signals with each other.
    """
    group = models.ManyToManyField(Group)
    name = models.CharField(max_length=128)
    timezone = models.CharField(max_length=32)
    shifts = models.ManyToManyField('Shift')


class Shift(SystemModel):
    """
    A Shift is used to record the beginning and the end of an experiment
    """
    name = models.CharField(max_length=128)
    ended_at = models.DateTimeField(null=True)

class LocalComputer(SystemModel):
    """
    A LocalComputer system is a cpu capable of loading a program, recording data from sensors and operating actuators.
    """
    group = models.ManyToManyField(Group)
    name = models.CharField(max_length=128)
    registration_token = models.CharField(max_length=128)
    secret_uuid = models.CharField(max_length=128)
    system = models.ForeignKey('System', null=True)
    command_refresh_sec = models.IntegerField(default=10)
    is_running = models.BooleanField(default=False)


# No-op
COMMAND_NOOP = 0
# shut down local_computer listener
COMMAND_DONE = 1
# load and start the indicated program on the local computer
COMMAND_LOAD_PROGRAM = 2
# stop the indicated program on the local computer
COMMAND_STOP_PROGRAM = 3


class Command(SystemModel):
    """
    Commands are enumerated json messages for LocalComputers.
    When command has been successfully executed, the is_executed flag is set to True
    """
    local_computer = models.ForeignKey('LocalComputer')
    type = models.IntegerField(default=COMMAND_NOOP, db_index=True)
    json_command = models.CharField(max_length="512", null=True)
    is_executed = models.BooleanField(default=False, db_index=True)

class Program(SystemModel):
    """
    A loadable script/code file that can be run on a local computer.
    A program will be run periodically with with a pause of the indicated
    sleep_time between sucessive runs.
    """
    group = models.ManyToManyField(Group)
    code = models.TextField(null=True)
    description = models.TextField(null=True)
    name = models.CharField(max_length=128)
    sleep_time_sec = models.FloatField(default=1.0)

class Map(SystemModel):
    """
    A map is a list of known signals with semantic meaning.
    """
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
BLOB_PROVIDER = file_provider

class Signal(SystemModel):
    """
    A time signal of floats.
    """
    group = models.ManyToManyField(Group)
    name = models.CharField(max_length=128, db_index=True)
    system = models.ForeignKey('System', null=True)
    local_computer = models.ForeignKey('LocalComputer', null=True)

    def add_points(self, data_points):
        """Add points to the signal
        :param data_points [[<float value>,<time in millisec>],...]
        """
        SIGNAL_PROVIDER.startup()
        SIGNAL_PROVIDER.append_data(self.uuid,
                                    ''.join(["[{:.15},{:.15}]".format(float(datum[0]),float(datum[1])) for datum in data_points]))


    def get_data(self):
        SIGNAL_PROVIDER.startup()
        data = SIGNAL_PROVIDER.get_blob(self.uuid)

        tokens = data.split("]")
        points = []
        for token in tokens:
            if token != '':
                ts = token[1:].split(",")
                points.append((float(ts[0]), float(ts[1])))
        return points

    @classmethod
    def millisec_to_utc(cls, millisec):
        return tmz.datetime.fromtimestamp(float(millisec), tz=pytz.UTC)

    @classmethod
    def utc_to_millisec(cls, dt):
        return delorean.Delorean(dt, timezone="UTC").epoch()

    def get_time_series(self):
        values, dates = self.get_data()
        return pd.TimeSeries(values, index=dates)

    def clear(self):
        SIGNAL_PROVIDER.startup()
        SIGNAL_PROVIDER.clear(self.uuid)


class Setting(SystemModel):
    group = models.ManyToManyField(Group)
    key = models.CharField(max_length=128, db_index=True)
    value = models.CharField(max_length=128)
    local_computer = models.ForeignKey('LocalComputer', null=True)
    system = models.ForeignKey('System', null=True)

    def __unicode__(self):
        return '{},{}'.format(self.key, self.value)


class Blob(SystemModel):
    group = models.ManyToManyField(Group)
    name = models.CharField(max_length=128, db_index=True)
    system = models.ForeignKey('System', null=True)
    local_computer = models.ForeignKey('LocalComputer', null=True)

    def get_data(self):
        BLOB_PROVIDER.startup()
        data = BLOB_PROVIDER.get_blob(self.uuid)
        return data

    def set_data(self, json_data):
        BLOB_PROVIDER.startup()
        BLOB_PROVIDER.write_blob(self.uuid, json_data)

@receiver(pre_save, sender=Command)
@receiver(pre_save, sender=LocalComputer)
@receiver(pre_save, sender=Map)
@receiver(pre_save, sender=MapPoint)
@receiver(pre_save, sender=Program)
@receiver(pre_save, sender=Shift)
@receiver(pre_save, sender=Signal)
@receiver(pre_save, sender=System)
@receiver(pre_save, sender=Setting)
@receiver(pre_save, sender=Event)
@receiver(pre_save, sender=Blob)
def set_uuid(sender, instance, **kwargs):
    """
    Register all SystemModel derived classes to set uuid
    """
    if not instance.uuid:
        instance.uuid = str(uuid4())
