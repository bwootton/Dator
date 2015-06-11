from robots.models import System

__author__ = 'brucewootton'
from django.test import TestCase

class TestModels(TestCase):


    def test_system_model_uuid(self):
        # with a derived system model
        asm = System.objects.create(name="a_name")
        # should have a UUID
        self.assertIsNotNone(asm.uuid)
        self.assertNotEqual(asm.uuid, "")

        # should have a created_at and updated_at
        self.assertIsNotNone(asm.created_at)
        self.assertIsNotNone(asm.updated_at)