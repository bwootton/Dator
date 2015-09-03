from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from data_api.models import System, Program, SystemModel, Map, LocalComputer, Command, Signal, Setting, Event
from django.utils.timezone import now
import json

class TestAPI(TestCase):

    def setUp(self):
        self.client = Client()

        # when creating a System
        self.system = System.objects.create(name="a_name")
        #

    def test_get_system(self):
        # should get the system
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'system', 'api_name': 'v1'})
        response = self.client.get(url)
        data = json.loads(response.content)["objects"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "a_name")

    def test_get_program(self):
        # should get a program.
        Program.objects.create(name="a program")
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'program', 'api_name': 'v1'})
        response = self.client.get(url)
        data = json.loads(response.content)["objects"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "a program")

    def test_post_local_computer(self):
        # should create a local computer.
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'local_computer', 'api_name': 'v1'})
        response = self.client.post(url,
                                    data=json.dumps({'name':"a_name",
                                                     'registration_token':'a_token',
                                                     'secret_uuid': 'a_uuid'}),
                                    content_type= "application/json"
                                    )
        lc = LocalComputer.objects.get(name='a_name')
        self.assertIsNotNone(lc)
        self.assertEqual(lc.secret_uuid, 'a_uuid')

class TestAPIWithLocalComputer(TestCase):

    def setUp(self):
        self.local_computer = LocalComputer.objects.create(name="a_name", registration_token= 'a_token')

    def test_filter_commands_by_local_computer(self):
        # with a local computer that has a command
        Command.objects.create(local_computer=self.local_computer )

        # should get the command
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'command', 'api_name': 'v1'})
        response = self.client.get(url, data={'local_computer_id': self.local_computer .id})
        r_data = json.loads(response.content)['objects']
        self.assertEquals(r_data[0]['id'], self.local_computer .id)

        # should only get the command for the given computer
        response = self.client.get(url, data={'local_computer_id':self.local_computer .id+1})
        r_data = json.loads(response.content)['objects']
        self.assertEquals(len(r_data), 0 )

    def test_filter_commands_by_is_executed(self):
        # with a local computer with executed and non-executed commands
        Command.objects.create(local_computer=self.local_computer , json_command='["is not executed"]', is_executed=False)
        Command.objects.create(local_computer=self.local_computer , json_command='["is executed"]', is_executed=True)

        # should get the command that is not executed.
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'command', 'api_name': 'v1'})
        response = self.client.get(url, data={'local_computer_id':self.local_computer.id, 'is_executed':False})
        r_data = json.loads(response.content)['objects']
        self.assertEquals(len(r_data), 1)
        self.assertEquals(r_data[0]['json_command'], '["is not executed"]')

        # should get the command that has been executed
        response = self.client.get(url, data={'local_computer_id':self.local_computer.id, 'is_executed':True})
        r_data = json.loads(response.content)['objects']
        self.assertEquals(len(r_data),1)
        self.assertEquals(r_data[0]['json_command'], '["is executed"]')


    def test_filter_signal_by_local_computer(self):
        # with a signal
        signal = Signal.objects.create(local_computer=self.local_computer, name="a_signal")
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'signal', 'api_name': 'v1'})

        # should get signal by local_computer
        response = self.client.get(url, data={'local_computer_id':self.local_computer.id})
        r_data = json.loads(response.content)['objects']
        self.assertEquals(r_data[0]['id'], signal.id)

    def test_filter_setting_by_local_computer(self):
        # with a setting
        setting = Setting.objects.create(local_computer=self.local_computer, key="a_signal", value="hello")
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'setting', 'api_name': 'v1'})

        response = self.client.get(url, data={'local_computer_id': self.local_computer.id})
        r_data = json.loads(response.content)['objects']
        self.assertEquals(r_data[0]['id'], setting.id)

    def test_filter_event_by_local_computer_and_time(self):
        # with an event
        event = Event.objects.create(local_computer=self.local_computer, type="a type", info="some info")
        after = now()
        event2 = Event.objects.create(local_computer=self.local_computer, type="type 2", info="some more info")

        # should filter events by computer created_at
        url = reverse("api_dispatch_list", kwargs={'resource_name': 'event', 'api_name': 'v1'})
        response = self.client.get(url, data={'local_computer_id': self.local_computer.id,
                'created_at__gt': after})
        r_data = json.loads(response.content)['objects']
        self.assertEquals(len(r_data), 1)
        self.assertEquals(r_data[0]['id'], event2.id)