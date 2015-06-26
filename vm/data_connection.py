import json
import uuid
import requests

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
        config["secret_uuid"] = str(uuid.uuid4())

        url = config['server'] + "/api/v1/local_computer/?format=json"
        response = requests.post(url, data=json.dumps(self.configurator.get_config()), headers=self.sec_header())
        new_config = json.loads(response.content)
        self.configurator.set_config(new_config)

    def update_config(self, config_location):
        """
        :param config_location: Location of local config file
        Update local config with global config.
        """
        config = self.configurator.get_config()
        url = config['server'] + "/api/v1/local_computer/{}/?format=json".format(config['id'])
        response = requests.get(url, headers= self.sec_header())
        if self.check_response_ok(response):
            updated_config = json.loads(response.content)
            for key in updated_config.keys():
                config[key] = updated_config[key]
            self.configurator.write_config(config_location)

    def set_local_computer_status(self, is_running):
        """
        :param isRunning:
        """
        config = self.configurator.get_config()
        config['is_running'] = is_running
        url = config['server'] + "/api/v1/local_computer/{}/?format=json".format(config['id'])
        response = requests.put(url, data=json.dumps(self.configurator.get_config()), headers=self.sec_header())



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

