import json
import requests


class Configurator(object):
    """
    A configurator is a class to manage a config for the Local Computer
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

    def __init__(self, configurator):
        self.configurator = configurator

    def register(self, registration_token=None, file_name=None):
        """
        Call to register a new local computer.
        """
        if registration_token:
            self.configurator.get_config()["registration_token"] = registration_token

        url = self.configurator.get_config()['server'] + "/api/v1/local_computer/?format=json"
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=json.dumps(self.configurator.get_config()), headers=headers)
        new_config = json.loads(response.content)
        self.configurator.set_config(new_config)



config = Configurator()
config.write_config("default.cfg")
data_connection = DataConnection(config)
data_connection.register("my reg token", "default.cfg")
