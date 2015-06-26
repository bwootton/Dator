import json
import os
from uuid import uuid4
import multiprocessing
import requests
import time


class Configurator(object):
    """
    Manages a config for the Local Computer
    """

    def __init__(self, **kwargs):
        if "filename" in kwargs:
            with open(kwargs["filename"], 'r') as input:
                self.config = json.loads(input.read())
        else:
            self.config = {
                'server': 'http://localhost:8000',
                'secret_uuid': '123412341234',
                'registration_token': 'abcd',
                'name': "a_local_computer"
            }

    def write_config(self, filename):
        """
        Save current config to a json file.
        """
        with open(filename, 'w') as output:
            output.write(json.dumps(self.config, indent=4))

    def get_config(self):
        return self.config

    def set_config(self, config):
        self.config = config


class DataConnection(object):
    def __init__(self, configurator):
        self.configurator = configurator

    def register(self, registration_token=None, file_name=None):
        """
        Call to register a new local computer.
        """
        config = self.configurator.get_config()
        if registration_token:
            config["registration_token"] = registration_token
        config["secret_uuid"] = str(uuid4())

        url = config['server'] + "/api/v1/local_computer/?format=json"
        response = requests.post(url, data=json.dumps(self.configurator.get_config()), headers=self.sec_header())
        new_config = json.loads(response.content)
        self.configurator.set_config(new_config)

    def update_config(self):
        """
        Update local config with global config.
        """
        config = self.configurator.get_config()
        url = config['server'] + "/api/v1/local_computer/{}/?format=json".format(config['id'])
        response = requests.get(url, headers= self.sec_header())
        if self.check_response_ok(response):
            updated_config = json.loads(response.content)
            for key in updated_config.keys():
                config[key] = updated_config[key]
            self.configurator.write_config(CONFIG_LOCATION)


    def get_new_commands(self):
        """
        :return: Commands from the server for this local computer that should be executed.
        """
        config = self.configurator.get_config()
        id = config["id"]
        url = "{}/api/v1/command/?format=json&is_local_computer_id={}&is_executed=false".format(config['server'], id)
        response = requests.get(url, headers = self.sec_header())
        if self.check_response_ok(response):
            return json.loads(response.content)['objects']
        return []

    def deactivate_command(self, command):
        config = self.configurator.get_config()
        id = config["id"]
        command['is_executed'] = True
        url = "{}/api/v1/command/{}/?format=json&is_local_computer_id={}&is_executed=false".format(config['server'], command['id'], id)
        response = requests.put(url, data=json.dumps(command), headers=self.sec_header())
        self.check_response_ok(response)

    def get_program(self, program_id):
        """
        :param program_id:
        :return: the program object or None if it doesn't exist
        """
        config = self.configurator.get_config()
        server = config["server"]
        url = "{}/api/v1/program/{}?format=json".format(program_id)
        response = server.get(url, headers = self.sec_header())
        if self.check_response_ok(response):
            return json.loads(response.content)
        return None

    def sec_header(self, base_header=None):
        auth_header = {'auth_key': self.configurator.get_config()["secret_uuid"], 'content-type': 'application/json'}
        if base_header is None:
            return auth_header
        auth_header.update(base_header)

    @classmethod
    def check_response_ok(cls, response):
        """
        :return: True if http response is a 200 class response.  False info otherwise.
        """
        if 200 <= response.status_code < 300:
            return True
        else:
            response_string = "WARNING Command lookup failed: status: {} reason: {}".format(response.status_code, response.reason)
            if response.content:
                response_string += response.content
            print response_string
            return False


CONFIG_LOCATION = "default.cfg"


def init_configurator():
    """
    Register local computer if not done previously.
    :return: The configurator for this local computer
    """
    if os.path.isfile(CONFIG_LOCATION):
        configurator = Configurator(filename=CONFIG_LOCATION)
        print "Found local configurator at {}".format(CONFIG_LOCATION)
    else:
        configurator = Configurator()
        configurator.write_config(CONFIG_LOCATION)

        data_connection = DataConnection(configurator)
        my_reg_token = str(uuid4())
        print "Registering to {} with token {}".format(configurator.get_config()['server'], my_reg_token)
        data_connection.register(my_reg_token, CONFIG_LOCATION)
        configurator.write_config(CONFIG_LOCATION)

    return configurator



def periodic_eval(refresh_time_sec, program, should_stop, shared_val):
    while not should_stop.value:
        shared_val.value += 1
        eval(compile(program, '<string>', 'exec'))

        time.sleep(refresh_time_sec)

    return periodic_eval


class WorkerPool(object):

    def __init__(self):
        self.job_list = {}
        self.shared_val = multiprocessing.Value('i',0)


    def start_program(self, program_id, refresh_time_sec, program):
        if program_id not in self.job_list.keys():
            should_stop = multiprocessing.Value('b', False)
            self.job_list[program_id] = [should_stop, multiprocessing.Process(target=periodic_eval, args=(refresh_time_sec, program, should_stop, self.shared_val))]
            self.job_list[program_id][1].start()

    def stop_program(self, program_id):
        self.job_list[program_id][0].value = True
        self.job_list[program_id][1].join(20)
        print "Stopped program id {}".format(program_id)

    def stop(self):
        for program_id in self.job_list.keys():
            self.stop_program(program_id)

COMMAND_NOOP = 0
COMMAND_DONE = 1
COMMAND_LOAD_PROGRAM = 2
COMMAND_STOP_PROGRAM = 3


class CommandHandler(object):
    def __init__(self, worker_pool, data_connection):
        self.worker_pool = worker_pool
        self.handler_map = {
            COMMAND_LOAD_PROGRAM: self.handle_load,
            COMMAND_STOP_PROGRAM: self.handle_stop,
        }


    def handle_commands(self, commands):
        done = False
        for command in commands:
            if command['type'] == COMMAND_NOOP:
                data_connection.deactivate_command(command)
                continue
            elif command['type'] == COMMAND_DONE:
                done = True
            else:
                self.handler_map[command['type']](command)
            data_connection.deactivate_command(command)
        return done


    def handle_load(self, command):
        print("got load")


    def handle_stop(self, command):
        print("go stop")


if __name__ == '__main__':
    """
    Main loop.  Handle commands until done.
    """
    configurator = init_configurator()
    data_connection = DataConnection(configurator)
    data_connection.update_config()
    worker_pool = WorkerPool()
    command_handler = CommandHandler(worker_pool, data_connection)

    done = False

    while not done:
        commands = data_connection.get_new_commands()
        done = command_handler.handle_commands(commands)
        time.sleep(configurator.get_config()['command_refresh_sec'])

    worker_pool.stop()
    print("got shared_value {}".format(worker_pool.shared_val.value))

    print("Received done command.  Shutting down.")




