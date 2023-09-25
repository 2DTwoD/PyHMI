import json
from threading import Timer

from tkinter import *
from types import SimpleNamespace
from PIL import Image, ImageTk

import di_conf.container as DI
from units.d_actuator import DActuator
from utils.structures import Coordinate


class ScreenCreator:
    def __init__(self):
        self.comm = DI.Container.communication()
        self.root = Tk()
        self.main_frame = Frame(self.root)
        self._screen = Canvas(self.main_frame, bg="black")
        self._update_period = 0

        self.mx = Label(self._screen, text=0, width=5)
        self.mx.place(x=0, y=0)
        self.my = Label(self._screen, text=0, width=5)
        self.my.place(x=0, y=20)
        self.root.bind('<Motion>', self.mouse_coordinates)

        with open('res/configuration/main.txt') as main_config_json:
            main_config = json.loads(main_config_json.read(), object_hook=lambda d: SimpleNamespace(**d))
            self.window_title = main_config.window_title
            self.resolution = main_config.resolution
            self.first_screen = main_config.first_screen
            self.screens = main_config.screens.__dict__
            self._update_period = max(main_config.update_period / 1000, 0.1)
            self._timer = Timer(self._update_period, self.update_all)
        self._curren_screen = self.first_screen

        self.d_actuators = {}
        self.d_actuators_pars = {}
        with open('res/configuration/units.txt') as units_json:
            units = json.loads(units_json.read(), object_hook=lambda d: SimpleNamespace(**d))
            self.d_actuators_pars = units.d_actuators.__dict__

        def on_close():
            self.comm.end()
            self.root.destroy()
            self._timer.cancel()
        self.root.protocol("WM_DELETE_WINDOW", on_close)

    def mouse_coordinates(self, event):
        self.mx.config(text=event.x)
        self.my.config(text=event.y)

    def start(self):
        self.root.title(self.window_title)
        self.root.geometry(self.resolution)
        background_img = ImageTk.PhotoImage(Image.open(self.screens[self.first_screen]))
        self._screen.create_image(background_img.width() / 2, background_img.height() / 2, image=background_img, tag="background")
        self._screen.config(width=background_img.width(), height=background_img.height())
        self._screen.place(x=0, y=0)

        for name, pars in self.d_actuators_pars.items():
            self.d_actuators[name] = DActuator(name, pars)

        def click(event):
            for d_actuator in self.d_actuators.values():
                d_actuator.left_click(event.x, event.y)
            # self.comm.send(10, [0, 1, 2, 3])
        #     screen.delete("motor")
        #     global count
        #     count += 1
        #     screen.create_image(191, 191, image=motors[count], tag="motor")
        #     if count == 2:
        #         count = -1
        self.screen.bind('<Button-1>', click)

        self._timer.start()

        self.main_frame.pack()
        self._screen.pack()
        self.root.mainloop()

    def update_all(self):
        for d_actuator in self.d_actuators.values():
            d_actuator.update()
        self._repeate()

    @property
    def screen(self):
        return self._screen

    def get_root_mouse_position(self):
        return Coordinate(self.screen.winfo_pointerx(), self.screen.winfo_pointery())

    @property
    def current_screen(self):
        return self._curren_screen

    def _repeate(self):
        self._timer = Timer(self._update_period, self.update_all)
        self._timer.start()
