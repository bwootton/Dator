from django.test import TestCase
from robots.models import System, Signal
import django.utils.timezone as tmz
import pytz
import delorean

class TestModel(TestCase):

    def setUp(self):
        # when creating a System
        self.system = System.objects.create(name="a_name")

    def test_set_uuid(self):
        # should set the uuid.
        self.assertIsNotNone(self.system.uuid)
        self.assertNotEquals(str(self.system.uuid), '')

    def test_create_timezone_aware(self):
        # should have a created_at and updated_at
        self.assertIsNotNone(self.system.created_at)
        self.assertIsNotNone(self.system.created_at.tzinfo)
        self.assertIsNotNone(self.system.updated_at)


    def test_reset_uuid(self):
        # should not reset the uuid on subsequent saves
        self.system.save()
        system2 = System.objects.get(uuid=self.system.uuid)
        self.assertIsNotNone(system2)

    def test_add_get_points(self):
        signal = Signal.objects.create(system=self.system,
                                       name='a_signal')
        n1 = Signal.utc_to_millisec(tmz.now())
        n2 = Signal.utc_to_millisec(tmz.now() + tmz.timedelta(seconds=1))
        signal.add_points([[1, n1], [2, n2]])
        points = signal._get_data()

        self.assertEqual(2, len(points))
        self.assertEqual(1,  points[0][0])
        self.assertEqual(2, points[1][0])
        self.assertAlmostEqual(n1, points[0][1],2)
        self.assertAlmostEqual(n2, points[1][1],2)

    def test_append_points(self):
        signal = Signal.objects.create(system=self.system,
                                       name='a_signal')
        n1 = Signal.utc_to_millisec(tmz.now())
        n2 = Signal.utc_to_millisec(tmz.now() + tmz.timedelta(seconds=1))
        signal.add_points([[1,n1]])
        signal.add_points([[2,n2]])


        points = signal._get_data()
        self.assertEqual(2, len(points))
        self.assertEqual(1,  points[0][0])
        self.assertEqual(2, points[1][0])
        self.assertAlmostEqual(n1, points[0][1],2)
        self.assertAlmostEqual(n2, points[1][1],2)


    def test_utc_time_functions(self):
        n1 = tmz.now()
        n1_ms = Signal.utc_to_millisec(n1)
        n1_back = Signal.millisec_to_utc(n1_ms)
        self.assertEqual(n1, n1_back)