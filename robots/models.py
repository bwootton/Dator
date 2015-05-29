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

class Controller(SystemModel):
    group = models.ManyToManyField(Group)
    name = models.CharField(max_length=128)
    system = models.ForeignKey('System')

class Command(SystemModel):
    controller = models.ForeignKey('Controller')

class Program(SystemModel):
    group = models.ManyToManyField(Group)
    code = models.TextField(null=True)
    description = models.TextField(null=True)
    name = models.CharField(max_length=128)


class Map(SystemModel):
    group = models.ManyToManyField(Group)
    name = models.CharField(max_length=128)
    controller = models.ForeignKey('Controller')

ACTUATOR = 1
SENSOR = 2


class MapPoint(SystemModel):
    map = models.ForeignKey('Map')
    point_type = models.IntegerField(default=SENSOR)
    name = models.CharField(max_length=128)
    path = models.CharField(max_length=128)
    controller = models.ForeignKey('Controller')


class Signal(SystemModel):
    group = models.ManyToManyField(Group)
    name = models.CharField(max_length=128)


class SignalBlob(SystemModel):
    signal = models.ForeignKey('Signal')

@receiver(post_save, sender=Command)
@receiver(post_save, sender=Controller)
@receiver(post_save, sender=Map)
@receiver(post_save, sender=MapPoint)
@receiver(post_save, sender=Program)
@receiver(post_save, sender=Shift)
@receiver(post_save, sender=Signal)
@receiver(post_save, sender=SignalBlob)
@receiver(post_save, sender=System)
def set_uuid(sender, instance, created, **kwargs):
    if created:
        instance.uuid = str(uuid4())
