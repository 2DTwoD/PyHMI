from tkinter import *

import di_conf.container as DI
from units.d_actuator import DActuator
from utils.cycle import Cycle
from utils.frame_canvas import FrameCanvas
from utils.structures import Coordinate, NameImage


class ScreenCreator(Tk):
    def __init__(self):
        super().__init__()
        self._com = DI.Container.communication()
        self._main_pars = DI.Container.main_pars()
        self._da_pars = DI.Container.da_pars()
        self._current_screen = self._main_pars.first_screen
        self._main_frame = Frame(self)
        self._screen = FrameCanvas(self._main_frame,
                                   NameImage(name='background',
                                             image_path=self._main_pars.screens[self._current_screen]))
        self.mx = Label(self._screen, text=0, width=5)
        self.mx.place(x=0, y=0)
        self.my = Label(self._screen, text=0, width=5)
        self.my.place(x=0, y=20)
        self.bind('<Motion>', self._mouse_coordinates_visu)

        self._connect_rect_canvas = Canvas(self._screen, width=20, height=20, highlightthickness=0)
        self._connect_rect = self._connect_rect_canvas.create_rectangle(0, 0, 20, 20, fill='red')
        self._connect_rect_canvas.place(x=self._main_pars.resolution.width - 20, y=0)

        self.d_actuators = {}

        self._cycle = Cycle(self._main_pars.update_period, self.update_all)

        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())

    def start(self):
        self.title(self._main_pars.window_title)
        self.geometry(self._main_pars.resolution.str_resolution)
        self.change_screen()

        for name in self._da_pars.get_names():
            self.d_actuators[name] = DActuator(name)

        self.bind('<Button-1>', self._screen_click_action)

        self._screen.pack(anchor=NW)
        self._main_frame.pack(fill="both", expand=True)
        self.mainloop()

    def _mouse_coordinates_visu(self, event):
        self.mx.config(text=event.x)
        self.my.config(text=event.y)

    def _screen_click_action(self, e):
        for d_actuator in self.d_actuators.values():
            d_actuator.left_click(self.get_mouse_position(relative=True))

    def change_screen(self):
        self._screen.new_image(NameImage(name="background",
                                         image_path=self._main_pars.screens[self._current_screen]))
        for d_actuator in self.d_actuators.values():
            d_actuator.change_screen()

    def update_all(self):
        self._connect_rect_canvas.itemconfig(self._connect_rect, fill='green' if self._com.connected else 'red')
        for d_actuator in self.d_actuators.values():
            d_actuator.update()

    def get_mouse_position(self, relative=False):
        if relative:
            return Coordinate(self._screen.winfo_pointerx() - self.winfo_rootx(), self._screen.winfo_pointery() - self.winfo_rooty())
        return Coordinate(self._screen.winfo_pointerx(), self._screen.winfo_pointery())

    @property
    def screen(self):
        return self._screen

    @property
    def current_screen(self):
        return self._current_screen

    def screen_add_image(self, image: NameImage, coordinate: Coordinate = Coordinate(0, 0), origin: str = 'nw'):
        self._screen.new_image(image, coordinate=coordinate, origin=origin)
