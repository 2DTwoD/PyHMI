import json
from types import SimpleNamespace

from utils.structures import Resolution


class MainParsService:
    def __init__(self):
        with open('res/configuration/main.txt', encoding='utf-8') as main_config_json:
            main_config = json.loads(main_config_json.read(), object_hook=lambda d: SimpleNamespace(**d))
            self.window_title = main_config.window_title
            self.resolution = Resolution(main_config.resolution)
            self.first_screen = main_config.first_screen
            self.screens = main_config.screens.__dict__
            self.update_period = max(main_config.update_period, 100)
