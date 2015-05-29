from tastypie.authentication import Authentication
from tastypie.fields import IntegerField, DateTimeField, CharField, BooleanField
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.resources import ALL_WITH_RELATIONS
from tastypie import fields
from robots.models import System, Program, Command, Controller


class SystemResource(ModelResource):

    class Meta:
        queryset = System.objects.all()
        authorization = Authorization()
        authentication = Authentication()
        resource_name = 'system'
        always_return_data = True


class ProgramResource(ModelResource):

    class Meta:
        queryset = Program.objects.all()
        authorization = Authorization()
        authentication = Authentication()
        resource_name = 'program'
        always_return_data = True


class CommandResource(ModelResource):

    class Meta:
        queryset = Command.objects.all()
        authorization = Authorization()
        authentication = Authentication()
        resource_name = 'command'
        always_return_data = True

class ControllerResource(ModelResource):

    class Meta:
        queryset = Controller.objects.all()
        authorization = Authorization()
        authentication = Authentication()
        resource_name = 'controller'
        always_return_data = True




