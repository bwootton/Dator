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
            output.write(json.dumps(self.config))

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
        if registration_token:
            self.configuration.get_config()["registration_token"] = registration_token

        url = self.configuration.get_config()['server'] + "/api/v1/local_computer/?format=json"
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(self.configuration.get_config()), headers=headers)
        new_config = json.loads(response.content)
        self.configuration.set_config(new_config)

    def get_new_commands(self):
        """
        :return: Commnds from the server to be executed
        """
        id = self.configuration.get_config()["id"]
        secret = self.configuration.get_config["secret_uuid"]
        url = "{}/api/v1/command/?format=json&is_local_computer_id={}&is_executed=false".format(
            self.configuration.get_config()['server'], id
        )
        response = requests.get(url, header={'auth_key': secret})
        return json.loads(response.content)['objects']


CONFIG_LOCATION = "default.cfg"


def init_config():
    """
    Register local computer if not done previously.
    :return: The configuration for this local computer
    """
    if os.path.isfile(CONFIG_LOCATION):
        configuration = Configuration(CONFIG_LOCATION)
        print "Found local configuration at {}".format(CONFIG_LOCATION)
    else:
        configuration = Configuration()
        configuration.write_config(CONFIG_LOCATION)

        data_connection = DataConnection(configuration)
        my_reg_token = str(uuid4())
        print "Registering to {} with token {}".format(configuration['server'], my_reg_token)
        data_connection.register("my reg token", CONFIG_LOCATION)
        configuration.write_config(CONFIG_LOCATION)

    return configuration


def create_workers(config):
    pass


def handle_commands(config):
    return True


if __name__ == '__main__':
    """
    Main loop.  Handle commands until done.
    """
    config = init_config()
    data_connection = DataConnection(config)
    done = False
    create_workers(config)
    while not done:
        # check for new commands every 10 seconds
        commands = data_connection.get_new_commands()
        done = handle_commands(commands)

    print("Received done command.  Shutting down.")




