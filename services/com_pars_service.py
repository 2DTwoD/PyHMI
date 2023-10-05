import json
from types import SimpleNamespace


class CommParsService:
    def __init__(self):
        with open('res/configuration/com.txt', encoding='utf-8') as comm_config_json:
            comm_config = json.loads(comm_config_json.read(), object_hook=lambda d: SimpleNamespace(**d))
            self.type = comm_config.type
            self.host = comm_config.host
            self.port = comm_config.port
            self.update_period = max(comm_config.update_period, 100)
