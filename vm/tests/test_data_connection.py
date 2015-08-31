import json
from django.test import LiveServerTestCase
from data_api.models import Command, LocalComputer, COMMAND_NOOP, Signal, System
from vm.base import Configurator
from vm.data_connection import DataConnection
import datetime
import pytz


class TestDataConnection(LiveServerTestCase):
    """
    Data Connection API Tests
    """
    def setUp(self):
        # With a configuration pointed to localhost
        self.local_computer = LocalComputer.objects.create(name="a_computer")

        self.configurator = Configurator()
        config = self.configurator.get_config()
        config['id'] = self.local_computer.id
        config['server'] = self.live_server_url

        self.data_connection = DataConnection(self.configurator)

    def tearDown(self):
        pass

    def test_get_new_commands(self):
        # with a new command
        json_command = json.dumps({'a':1, 'b':'c'})
        Command.objects.create(type=COMMAND_NOOP, local_computer=self.local_computer, json_command=json_command)

        # should get command
        commands = self.data_connection.get_new_commands()
        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0]['type'], COMMAND_NOOP)
        self.assertEqual(commands[0]['json_command'], json_command)

    def test_add_signal_points(self):
        signal = Signal.objects.create(name='a_signal')
        n1 = Signal.utc_to_millisec(datetime.datetime.now(tz=pytz.UTC))
        n2 = Signal.utc_to_millisec(datetime.datetime.now(tz=pytz.UTC) + datetime.datetime.timedelta(seconds=1))
        json_data = json.dumps([[1, n1], [2, n2]])
        self.data_connection.add_signal_points(signal.id)

        points = signal.get_data()
        self.assertEqual(2, len(points))
        self.assertEqual(1,  points[0][0])
        self.assertEqual(2, points[1][0])
        self.assertAlmostEqual(n1, points[0][1], 2)
        self.assertAlmostEqual(n2, points[1][1], 2)

    def test_add_signal_points_by_name(self):
        signal = Signal.objects.create(name='a_signal', local_computer=self.local_computer)
        n1 = Signal.utc_to_millisec(datetime.datetime.now(tz=pytz.UTC))
        n1 = Signal.utc_to_millisec(datetime.datetime.now(tz=pytz.UTC))
        n2 = Signal.utc_to_millisec(datetime.datetime.now(tz=pytz.UTC) + datetime.datetime.timedelta(seconds=1))
        json_data = json.dumps([[1, n1], [2, n2]])
        self.data_connection.add_signal_points_by_name(signal.name)

        points = signal.get_data()
        self.assertEqual(2, len(points))
        self.assertEqual(1,  points[0][0])
        self.assertEqual(2, points[1][0])
        self.assertAlmostEqual(n1, points[0][1], 2)
        self.assertAlmostEqual(n2, points[1][1], 2)



