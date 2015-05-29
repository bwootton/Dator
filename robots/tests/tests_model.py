from django.test import TestCase
from robots.models import System


class TestModel(TestCase):

    def setUp(self):
        # when creating a System
        self.system = System.objects.create(name="a_name")

    def test_set_uuid(self):
        # should set the uuid.
        self.assertIsNotNone(self.system.uuid)
        self.assertNotEquals(str(self.system.uuid), '')


    def test_reset_uuid(self):
        # should not reset the uuid on subsequent saves
        self.system.save()
        system2 = System.objects.get(uuid=self.system.uuid)
        self.assertIsNotNone(system2)


