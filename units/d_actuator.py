from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk
import di_conf.container as DI
from services.d_actuator_service import DActuatorService
from utils.structures import NameImage, Coordinate, Area, Dimension


class DActuator:
    def __init__(self, name, parameters):
        self.sc = DI.Container.screen_creator()
        self.name = name
        self.stop_img = NameImage(name=self.name + "_stop", image=ImageTk.PhotoImage(Image.open(parameters.img_path.stop)))
        self.start_img = NameImage(name=self.name + "_start", image=ImageTk.PhotoImage(Image.open(parameters.img_path.start)))
        self.alarm_img = NameImage(name=self.name + "_alarm", image=ImageTk.PhotoImage(Image.open(parameters.img_path.alarm)))

        self.location = {}
        for screen_name, location in parameters.location.__dict__.items():
            self.location[screen_name] = Coordinate(location.x, location.y)
        self.width = parameters.dimension.width
        self.height = parameters.dimension.height
        self.current_img = self.stop_img
        self.image_dimension = Dimension(max(self.stop_img.width(), self.start_img.width(), self.alarm_img.width()),
                                         max(self.stop_img.height(), self.start_img.height(), self.alarm_img.height()))
        self.plc_data = DActuatorService(parameters.start_address, parameters.start_address + 7)
        self.click_area = Area()
        self.window = None

    def update(self):
        if self.sc.current_screen not in self.location:
            return
        # self.plc_data.update()
        if self.sc.screen.find_withtag(self.name) == ():
            x = self.location[self.sc.current_screen].x
            y = self.location[self.sc.current_screen].y
            self.sc.create_image(x, y, self.current_img.image, self.current_img.name)
            self.click_area.update(y - self.image_dimension.height / 2, y + self.image_dimension.height / 2,
                                   x - self.image_dimension.width / 2, x + self.image_dimension.width / 2)
        print(self.plc_data)

    def close_window(self):
        self.window.destroy()
        self.window = None

    def left_click(self, mouse_x, mouse_y):
        self.sc.comm.send(0, [1, 2, 3, 4, 5, 6, 7, 8])
        if self.click_area.left < mouse_x < self.click_area.right and \
                self.click_area.down > mouse_y > self.click_area.up:
            if self.window is None:
                self.get_new_window()
            self.window.deiconify()
            self.window.focus_set()
            root_mouse = self.sc.get_root_mouse_position()
            self.window.geometry(f"350x400+{root_mouse.x}+{root_mouse.y}")

    def get_new_window(self):
        self.window = Toplevel(self.sc.screen)
        self.window.title(self.name)
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        self.window.attributes("-topmost", True)
        self.window.resizable(False, False)
        pages = ttk.Notebook(self.window)
        pages.pack(expand=True, fill=BOTH)
        page1 = self._add_page(pages, ttk.Frame(pages), "Control")
        page2 = self._add_page(pages, ttk.Frame(pages), "Locks")
        page3 = self._add_page(pages, ttk.Frame(pages), "Auto conditions")
        page4 = self._add_page(pages, ttk.Frame(pages), "Errors")
        page5 = self._add_page(pages, ttk.Frame(pages), "Service")

    @staticmethod
    def _add_page(pages: ttk.Notebook, page: Frame, title: str):
        page.pack(fill=BOTH, expand=True)
        pages.add(page, text=title)
        return page


