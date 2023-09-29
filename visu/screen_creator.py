from tkinter import *
from PIL import Image, ImageTk

import di_conf.container as DI
from units.d_actuator import DActuator
from utils.cycle import Cycle
from utils.structures import Coordinate, NameImage


class ScreenCreator:
    def __init__(self):
        self._com = DI.Container.communication()
        self._main_pars = DI.Container.main_pars()
        self._units_pars = DI.Container.units_pars()
        self.root = Tk()
        self.main_frame = Frame(self.root)
        self._screen = Canvas(self.main_frame, bg="black", highlightthickness=0)
        self._update_period = 0

        self.mx = Label(self._screen, text=0, width=5)
        self.mx.place(x=0, y=0)
        self.my = Label(self._screen, text=0, width=5)
        self.my.place(x=0, y=20)
        self.root.bind('<Motion>', self.mouse_coordinates)

        self._curren_screen = self._main_pars.first_screen

        self.connect_rect_canvas = Canvas(self._screen, width=20, height=20, highlightthickness=0)
        self.connect_rect = self.connect_rect_canvas.create_rectangle(0, 0, 20, 20, fill='red')
        self.connect_rect_canvas.place(x=self._main_pars.resolution.width - 20, y=0)

        self.d_actuators = {}
        self.d_actuators_pars = {}

        self._cycle = Cycle(self._update_period, self.update_all)

        self.root.protocol("WM_DELETE_WINDOW", lambda: self.root.destroy())

    def mouse_coordinates(self, event):
        self.mx.config(text=event.x)
        self.my.config(text=event.y)

    def start(self):
        self.root.title(self._main_pars.window_title)
        self.root.geometry(self._main_pars.resolution.str_resolution)
        background_img = ImageTk.PhotoImage(Image.open(self._main_pars.screens[self._main_pars.first_screen]))
        self._screen.create_image(background_img.width() / 2, background_img.height() / 2, image=background_img, tag="background")
        self._screen.config(width=background_img.width(), height=background_img.height())
        self._screen.place(x=0, y=0)

        for name in self._units_pars.get_d_actuators_names():
            self.d_actuators[name] = DActuator(name)

        def click(event):
            for d_actuator in self.d_actuators.values():
                d_actuator.left_click(event.x, event.y)

        self.screen.bind('<Button-1>', click)

        self._screen.pack()
        self.main_frame.place(x=0, y=0)
        self.root.mainloop()

    def update_all(self):
        self.connect_rect_canvas.itemconfig(self.connect_rect, fill='green' if self._com.connected else 'red')
        for d_actuator in self.d_actuators.values():
            d_actuator.update()

    @property
    def screen(self):
        return self._screen

    def get_root_mouse_position(self):
        return Coordinate(self.screen.winfo_pointerx(), self.screen.winfo_pointery())

    @property
    def current_screen(self):
        return self._curren_screen

    def screen_add_image(self, x: int, y: int, image: NameImage):
        if self.screen.find_withtag(image.name):
            self.screen.delete(image.name)
        self.screen.create_image(x, y, image=image.image, tag=image.name)

