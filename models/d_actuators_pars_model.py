import json
from types import SimpleNamespace

from utils.structures import Dimension


class DActuatorsParsData:
    def __init__(self):
        with open('res/configuration/d_actuators.txt') as units_json:
            d_actuators = json.loads(units_json.read(), object_hook=lambda d: SimpleNamespace(**d))
            d_actuators_pars = d_actuators.__dict__
            self.names = list(d_actuators_pars)
            self.location = d_actuators_pars.location.__dict__
            self.dimension = Dimension(d_actuators_pars.dimension.width, d_actuators_pars.dimension.height)
            self.img_path = d_actuators_pars.img_path.__dict__
            self.start_address = d_actuators_pars.start_address


    def get_names(self) -> list:
        return self.names

    def get(self, name: str = ''):
        pass
        #return self._d_actuators_pars[name]