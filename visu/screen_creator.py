from tkinter import *

import di_conf.container as DI
from units.d_actuator import DActuator
from utils.cycle import Cycle
from utils.frame_canvas import FrameCanvas
from utils.structures import Coordinate, NameImage
from visu.chapter_panel import ChapterPanel
from visu.service_panel import ServicePanel


class ScreenCreator(Tk):
    def __init__(self):
        super(ScreenCreator, self).__init__()
        self._com = DI.Container.communication()
        self._main_pars = DI.Container.main_pars()
        self._da_pars = DI.Container.da_pars()
        self._current_screen = self._main_pars.first_screen
        self._main_frame = Frame(self)

        self._service_panel: ServicePanel = None
        self._cycle: Cycle = None
        self._screen = FrameCanvas(self._main_frame,
                                   NameImage(name='background',
                                             image_path=self._main_pars.screens[self._current_screen]))
        self._chapters = ChapterPanel(self._main_frame)
        self.d_actuators = {}

        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())

    def start(self):
        self.title(self._main_pars.window_title)
        self.geometry(self._main_pars.resolution.str_resolution)
        self.change_screen()

        for name in self._da_pars.get_names():
            self.d_actuators[name] = DActuator(name)

        self.bind('<Button-1>', self._screen_click_action)

        self._service_panel = ServicePanel(self._main_frame)

        self._cycle = Cycle(self._main_pars.update_period, self.update_all)

        self._service_panel.pack(side=TOP, fill="both", expand=True)
        self._chapters.pack(side=TOP, fill="both", expand=True)
        self._screen.pack(side=TOP, anchor=NW)
        self._main_frame.pack(fill="both", expand=True)
        self.mainloop()

    def _screen_click_action(self, event):
        for d_actuator in self.d_actuators.values():
            d_actuator.left_click(Coordinate(event.x, event.y))

    def change_screen(self):
        self._screen.new_image(NameImage(name="background",
                                         image_path=self._main_pars.screens[self._current_screen]))
        for d_actuator in self.d_actuators.values():
            d_actuator.change_screen()

    def update_all(self):
        self._service_panel.refresh()
        for d_actuator in self.d_actuators.values():
            d_actuator.update()

    def get_mouse_position(self, relative=False):
        if relative:
            return Coordinate(self.winfo_pointerx() - self.winfo_rootx(), self.winfo_pointery() - self.winfo_rooty())
        return Coordinate(self.winfo_pointerx(), self.winfo_pointery())

    @property
    def screen(self):
        return self._screen

    @property
    def current_screen(self):
        return self._current_screen

    def screen_add_image(self, image: NameImage, coordinate: Coordinate = Coordinate(0, 0), origin: str = 'nw'):
        self._screen.new_image(image, coordinate=coordinate, origin=origin)
