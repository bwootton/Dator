from uuid import uuid4
from django.db import models
from django.contrib.auth.models import Group
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

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
    #secret_uuid = models.CharField(max_length=128)
    system = models.ForeignKey('System', null=True)


class Command(SystemModel):
    local_computer = models.ForeignKey('LocalComputer')
    command_type = models.IntegerField()
    json_command = models.CharField(max_length="512")
    is_executed = models.BooleanField(default=False)

class Program(SystemModel):
    group = models.ManyToManyField(Group)
    code = models.TextField(null=True)
    description = models.TextField(null=True)
    name = models.CharField(max_length=128)


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


class Signal(SystemModel):
    group = models.ManyToManyField(Group)
    name = models.CharField(max_length=128)



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
def set_uuid(sender, instance, **kwargs):
    if not instance.uuid:
        instance.uuid = str(uuid4())
