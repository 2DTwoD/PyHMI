import json
from types import SimpleNamespace


class CommParsData:
    def __init__(self):
        with open('res/configuration/com.txt') as comm_config_json:
            comm_config = json.loads(comm_config_json.read(), object_hook=lambda d: SimpleNamespace(**d))
            self.type = comm_config.type
            self.host = comm_config.host
            self.port = comm_config.port
            self.update_period = comm_config.update_period / 1000.0
