from django.test import TestCase, Client
from robots.models import System, Program, SystemModel, Map, LocalComputer, Command, Signal
import json

class TestAPI(TestCase):

    def setUp(self):
        self.client = Client()

        # when creating a System
        self.system = System.objects.create(name="a_name")

    def test_get_system(self):
        # should get the system
        response = self.client.get("/api/v1/system/?format=json")
        data = json.loads(response.content)["objects"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "a_name")

    def test_get_program(self):
        Program.objects.create(name="a program")
        response = self.client.get("/api/v1/program/?format=json")
        data = json.loads(response.content)["objects"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "a program")

    def test_post_local_computer(self):
        response = self.client.post("/api/v1/local_computer/?format=json",
                                    data=json.dumps({'name':"a_name",
                                                     'registration_token':'a_token',
                                                     'secret_uuid': 'a_uuid'}),
                                    content_type= "application/json"
                                    )
        lc = LocalComputer.objects.get(name='a_name')
        self.assertIsNotNone(lc)
        self.assertEqual(lc.secret_uuid, 'a_uuid')

    def test_filter_commands_by_local_computer(self):
        local_computer = LocalComputer.objects.create(name="a_name", registration_token= 'a_token')
        command = Command.objects.create(local_computer=local_computer)
        response = self.client.get("/api/v1/command/?format=json&local_computer_id={}".format(local_computer.id))
        r_data = json.loads(response.content)['objects']
        self.assertEquals(r_data[0]['id'], local_computer.id)

        response = self.client.get("/api/v1/command/?format=json&local_computer_id={}".format(local_computer.id+1))
        r_data = json.loads(response.content)['objects']
        self.assertEquals(len(r_data), 0 )

    def test_filter_commands_by_is_executed(self):
        local_computer = LocalComputer.objects.create(name="a_name", registration_token= 'a_token')
        command = Command.objects.create(local_computer=local_computer, is_executed=False)
        response = self.client.get("/api/v1/command/?format=json&local_computer_id={}&is_executed=false".format(local_computer.id))
        r_data = json.loads(response.content)['objects']
        self.assertEquals(r_data[0]['id'], local_computer.id)

        response = self.client.get("/api/v1/command/?format=json&local_computer_id={}&is_executed=true".format(local_computer.id))
        r_data = json.loads(response.content)['objects']
        self.assertEquals(len(r_data), 0 )

    def test_filter_signal_by_local_computer(self):
        local_computer = LocalComputer.objects.create(name="a_name", registration_token= 'a_token')
        signal = Signal.objects.create(local_computer=local_computer, name="a_signal")
        response = self.client.get("/api/v1/signal/?format=json&local_computer_id={}".format(local_computer.id))
        self.assertContains(response, "a_signal")
        r_data = json.loads(response.content)['objects']
        self.assertEquals("a_signal", r_data[0]['name'])

    def test_filter_setting_by_local_computer(self):
        local_computer = LocalComputer.objects.create(name="a_name", registration_token= 'a_token')
        signal = System.objects.create(local_computer=local_computer, key="a_signal", value="hello")
        response = self.client.get("/api/v1/setting/?format=json&local_computer_id={}".format(local_computer.id))
        self.assertContains(response, "a_signal")
        r_data = json.loads(response.content)['objects']
        self.assertEquals("a_signal", r_data[0]['name'])
