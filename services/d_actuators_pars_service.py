import json
from types import SimpleNamespace

from PIL import Image, ImageTk

from utils.structures import Dimension, Coordinate, NameImage


class DActuatorsParsService:
    def __init__(self):
        with open('res/configuration/d_actuators.txt') as units_json:
            d_actuators_struct = json.loads(units_json.read(), object_hook=lambda d: SimpleNamespace(**d))
            self._names = list(d_actuators_struct.__dict__)
            self._d_actuators = {}
            for name, par in d_actuators_struct.__dict__.items():
                self._d_actuators[name] = {
                    'location': dict(map(lambda pair: (pair[0], Coordinate(pair[1].x, pair[1].y)),
                                         par.location.__dict__.items())),
                    'dimension': Dimension(par.dimension.width, par.dimension.height),
                    'img_path': par.img_path.__dict__,
                    'start_address': par.start_address}

    def get_names(self) -> list:
        return self._names

    def get_location(self, name: str) -> dict:
        return self._d_actuators[name]['location']

    def get_dimension(self, name: str) -> Dimension:
        return self._d_actuators[name]['dimension']

    def get_name_img(self, name: str, status: str) -> NameImage:
        try:
            result = NameImage(name=name,
                               image=ImageTk.PhotoImage(Image.open(self._d_actuators[name]['img_path'].get(status, 'none'))))
        except:
            print(f'No path for {name} {status} image')
            result = NameImage(name=name,
                               image=ImageTk.PhotoImage(Image.open('res/pics/common/unknown.png')))
        return result

    def get_start_address(self, name: str) -> int:
        return self._d_actuators[name]['start_address']
