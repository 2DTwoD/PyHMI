from tkinter import *
from PIL import Image, ImageTk

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
        self._main_frame = Frame(self)
        self._frame_for_objects = Frame(self._main_frame)

        self.mx = Label(self._frame_for_objects, text=0, width=5)
        self.mx.place(x=0, y=0)
        self.my = Label(self._frame_for_objects, text=0, width=5)
        self.my.place(x=0, y=20)
        self.bind('<Motion>', self._mouse_coordinates_visu)

        self._current_screen = self._main_pars.first_screen
        self.background_img =
        self._screen = FrameCanvas(self._main_frame,
                                   NameImage(name='background',
                                             image=ImageTk.PhotoImage(Image.open(self._main_pars.screens[self._current_screen]))))
        # Canvas(self._main_frame, bg="black", highlightthickness=0)

        self._connect_rect_canvas = Canvas(self._main_frame, width=20, height=20, highlightthickness=0)
        self._connect_rect = self._connect_rect_canvas.create_rectangle(0, 0, 20, 20, fill='red')
        self._connect_rect_canvas.place(x=self._main_pars.resolution.width - 20, y=0)

        self.d_actuators = {}

        self._cycle = Cycle(self._main_pars.update_period, self.update_all)

        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())

    def start(self):
        self.title(self._main_pars.window_title)
        self.geometry(self._main_pars.resolution.str_resolution)
        self.change_screen()
        # self._screen.create_image(background_img.width() / 2, background_img.height() / 2, image=background_img, tag="background")
        # self._screen.config(width=background_img.width(), height=background_img.height())

        for name in self._da_pars.get_names():
            self.d_actuators[name] = DActuator(name)

        self._screen.bind('<Button-1>', self._screen_click_action)

        self._screen.pack()
        # self._frame_for_objects.place(x=0, y=0)
        self._main_frame.place(x=0, y=0)
        self.mainloop()

    def _mouse_coordinates_visu(self, event):
        self.mx.config(text=event.x)
        self.my.config(text=event.y)

    def _screen_click_action(self, event):
        for d_actuator in self.d_actuators.values():
            d_actuator.left_click(event.x, event.y)

    def change_screen(self):
        self.background_img = ImageTk.PhotoImage(Image.open(self._main_pars.screens[self._current_screen]))
        self._screen.new_image(NameImage(name="background", image=self.background_img))
        for d_actuator in self.d_actuators.values():
            d_actuator.change_screen()

    def update_all(self):
        self._connect_rect_canvas.itemconfig(self._connect_rect, fill='green' if self._com.connected else 'red')
        for d_actuator in self.d_actuators.values():
            d_actuator.update()

    def get_root_mouse_position(self):
        return Coordinate(self.screen.winfo_pointerx(), self.screen.winfo_pointery())

    @property
    def frame_for_objects(self):
        return self._frame_for_objects

    @property
    def screen(self):
        return self._screen

    @property
    def current_screen(self):
        return self._current_screen

    # def screen_add_image(self, x: int, y: int, image: NameImage):
    #     if self.screen.find_withtag(image.name):
    #         self.screen.delete(image.name)
    #     self.screen.create_image(x, y, image=image.image, tag=image.name)
