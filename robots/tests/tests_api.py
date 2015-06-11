from django.test import TestCase, Client
from robots.models import System, Program, SystemModel, Map
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


