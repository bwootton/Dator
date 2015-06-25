import json
import os
from uuid import uuid4
import requests


class Configuration(object):
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
    def __init__(self, configuration):
        self.configuration = configuration

    def register(self, registration_token=None, file_name=None):
        """
        Call to register a new local computer.
        """
        config = self.configuration.get_config()
        if registration_token:
            config["registration_token"] = registration_token
        config["secret_uuid"] = str(uuid4())\

        url = config['server'] + "/api/v1/local_computer/?format=json"
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(self.configuration.get_config()), headers=headers)
        new_config = json.loads(response.content)
        self.configuration.set_config(new_config)

    def update_config(self):
        """
        Update local config with global config.
        """
        config = self.configuration.get_config()
        url = config['server'] + "/api/v1/local_computer/{}/?format=json".format(config['id'])



    def get_new_commands(self):
        """
        :return: Commnds from the server to be executed
        """
        config = self.configuration.get_config()
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


def init_config():
    """
    Register local computer if not done previously.
    :return: The configuration for this local computer
    """
    if os.path.isfile(CONFIG_LOCATION):
        configuration = Configuration(filename=CONFIG_LOCATION)
        print "Found local configuration at {}".format(CONFIG_LOCATION)
    else:
        configuration = Configuration()
        configuration.write_config(CONFIG_LOCATION)

        data_connection = DataConnection(configuration)
        my_reg_token = str(uuid4())
        print "Registering to {} with token {}".format(configuration.get_config()['server'], my_reg_token)
        data_connection.register(my_reg_token, CONFIG_LOCATION)
        configuration.write_config(CONFIG_LOCATION)

    return configuration


class WorkerPool(object):

    def __init__(self, config):
        pass


    def stop(self):
        pass


def handle_commands(config, worker_pool):
    return True


if __name__ == '__main__':
    """
    Main loop.  Handle commands until done.
    """
    config = init_config()
    data_connection = DataConnection(config)
    done = False
    worker_pool = WorkerPool(config)
    while not done:
        commands = data_connection.get_new_commands()
        done = handle_commands(commands, worker_pool)


    worker_pool.stop()
    print("Received done command.  Shutting down.")




