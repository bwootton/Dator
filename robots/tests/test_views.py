from django.test import TestCase, Client
from robots.models import System, Signal


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        # when creating a System
        self.system = System.objects.create(name="a_name")

