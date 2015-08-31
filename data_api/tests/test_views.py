import json
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from data_api.models import System, Signal, LocalComputer
import django.utils.timezone as tmz


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        # when creating a System
        self.system = System.objects.create(name="a_name")
        self.local_computer = LocalComputer.objects.create(name="local_computer")
        self.client = Client()

    def test_get_points(self):
        signal = Signal.objects.create(system=self.system, name='a_signal')
        n1 = Signal.utc_to_millisec(tmz.now())
        n2 = Signal.utc_to_millisec(tmz.now() + tmz.timedelta(seconds=1))
        signal.add_points([[1, n1], [2, n2]])

        a = reverse('signal_data', args=(signal.id,))
        response = self.client.get(reverse('signal_data', args=(signal.id,)))
        points = json.loads(response.content)

        self.assertEqual(2, len(points))
        self.assertEqual(1,  points[0][0])
        self.assertEqual(2, points[1][0])
        self.assertAlmostEqual(n1, points[0][1], 2)
        self.assertAlmostEqual(n2, points[1][1], 2)

    def test_append_points(self):
        signal = Signal.objects.create(system=self.system, name='a_signal')
        n1 = Signal.utc_to_millisec(tmz.now())
        n2 = Signal.utc_to_millisec(tmz.now() + tmz.timedelta(seconds=1))
        a = reverse('signal_data', args=(signal.id,))
        json_data = json.dumps([[1, n1], [2, n2]])
        response = self.client.post(reverse('signal_data', args=(signal.id,)), data=json_data,
                                    content_type="application/json")
        points = signal.get_data()
        self.assertEqual(2, len(points))
        self.assertEqual(1,  points[0][0])
        self.assertEqual(2, points[1][0])
        self.assertAlmostEqual(n1, points[0][1], 2)
        self.assertAlmostEqual(n2, points[1][1], 2)