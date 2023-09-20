import json
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
        self._curren_screen = self.first_screen

        self.motors = {}
        self.motors_pars = {}
        with open('res/configuration/units.txt') as units_json:
            units = json.loads(units_json.read(), object_hook=lambda d: SimpleNamespace(**d))
            self.motors_pars = units.motors.__dict__

        def on_close():
            self.comm.end()
            self.root.destroy()
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

        for motor_name, motor_pars in self.motors_pars.items():
            self.motors[motor_name] = DActuator(motor_name, motor_pars)
            self.motors[motor_name].update()

        def click(event):
            for motor_name, motor_pars in self.motors_pars.items():
                self.motors[motor_name].left_click(event.x, event.y)
            # self.comm.send(10, [0, 1, 2, 3])
        #     screen.delete("motor")
        #     global count
        #     count += 1
        #     screen.create_image(191, 191, image=motors[count], tag="motor")
        #     if count == 2:
        #         count = -1
        self.screen.bind('<Button-1>', click)

        self.main_frame.pack()
        self._screen.pack()
        self.root.mainloop()

    @property
    def screen(self):
        return self._screen

    def get_root_mouse_position(self):
        return Coordinate(self.screen.winfo_pointerx(), self.screen.winfo_pointery())

    @property
    def current_screen(self):
        return self._curren_screen
