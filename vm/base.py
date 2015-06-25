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
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(self.configurator.get_config()), headers=headers)
        new_config = json.loads(response.content)
        self.configurator.set_config(new_config)

    def update_config(self):
        """
        Update local config with global config.
        """
        config = self.configurator.get_config()
        url = config['server'] + "/api/v1/local_computer/{}/?format=json".format(config['id'])
        response = requests.get(url, headers={'content-type': 'application/json', 'auth_key': config['secret_uuid']})
        if 200 <= response.status_code < 300:
            updated_config = json.loads(response.content)
            for key in updated_config.keys():
                config[key] = updated_config[key]
            self.configurator.write_config(CONFIG_LOCATION)
        else:
            print "WARNING Config Lookup failed: status: {} reason: {}".format(response.status_code, response.reason)
            if response.content:
                print response.content
            return []

    def get_new_commands(self):
        """
        :return: Commands from the server for this local computer that should be executed.
        """
        config = self.configurator.get_config()
        id = config["id"]
        secret_uuid = config["secret_uuid"]
        url = "{}/api/v1/command/?format=json&is_local_computer_id={}&is_executed=false".format(config['server'], id)
        response = requests.get(url, headers={'auth_key': secret_uuid})
        if 200 <= response.status_code < 300:
            return json.loads(response.content)['objects']
        else:
            print "WARNING Command lookup failed: status: {} reason: {}".format(response.status_code, response.reason)
            if response.content:
                print response.content
            return []


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


def handle_commands(config, worker_pool):
    return True


if __name__ == '__main__':
    """
    Main loop.  Handle commands until done.
    """
    configurator = init_configurator()
    data_connection = DataConnection(configurator)
    data_connection.update_config()
    worker_pool = WorkerPool()

    done = False
    worker_pool.start_program(1, 1, "print('hello world')")

    for i in range(1):
        commands = data_connection.get_new_commands()
        done = handle_commands(commands, worker_pool)
        time.sleep(configurator.get_config()['command_refresh_sec'])

    worker_pool.stop()
    print("got shared_value {}".format(worker_pool.shared_val.value))

    print("Received done command.  Shutting down.")




