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
        self.win_dimension = Dimension(350, 400)
        self.current_img = self.stop_img
        self.image_dimension = Dimension(max(self.stop_img.width(), self.start_img.width(), self.alarm_img.width()),
                                         max(self.stop_img.height(), self.start_img.height(), self.alarm_img.height()))
        self.plc_data = DActuatorService(parameters.start_address, parameters.start_address + 7)
        self.click_area = Area()
        self.window = None

    def update(self):
        if self.sc.current_screen not in self.location:
            return
        self.plc_data.update()
        if self.sc.screen.find_withtag(self.name) == ():
            x = self.location[self.sc.current_screen].x
            y = self.location[self.sc.current_screen].y
            self.sc.create_image(x, y, self.current_img.image, self.current_img.name)
            self.click_area.update(y - self.image_dimension.height / 2, y + self.image_dimension.height / 2,
                                   x - self.image_dimension.width / 2, x + self.image_dimension.width / 2)
        # print(self.plc_data)

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
            self.window.geometry(
                f"{self.win_dimension.width}x{self.win_dimension.height}+{root_mouse.x}+{root_mouse.y}")


    def get_new_window(self):
        self.window = Toplevel(self.sc.screen)
        self.window.title(self.name)
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        self.window.attributes("-topmost", True)
        self.window.resizable(False, False)

        pages = ttk.Notebook(self.window)
        page1 = self._add_page(pages, ttk.Frame(pages), "Control")
        page2 = self._add_page(pages, ttk.Frame(pages), "Locks")
        page3 = self._add_page(pages, ttk.Frame(pages), "Auto conditions")
        page4 = self._add_page(pages, ttk.Frame(pages), "Errors")
        page5 = self._add_page(pages, ttk.Frame(pages), "Service")
        status_picture = Canvas(page1, width=self.image_dimension.width,
                                height=self.image_dimension.height,
                                highlightthickness=0)
        status_picture.create_image(self.image_dimension.width / 2,
                                    self.image_dimension.height / 2,
                                    image=self.stop_img.image,
                                    tag="motor_status")
        start_button = Button(page1, text='Старт')
        stop_button = Button(page1, text='Стоп')
        auto_button = Button(page1, text='Автомат')
        manual_button = Button(page1, text='Ручной')
        for i in range(10):
            page1.grid_columnconfigure(i, minsize=self.win_dimension.width / 10)
            page1.grid_rowconfigure(i, minsize=self.win_dimension.height / 10)
        status_picture.grid(row=0, column=4, columnspan=3, sticky=NSEW)
        start_button.grid(row=1, column=2, columnspan=3, sticky=NSEW)
        stop_button.grid(row=1, column=5, columnspan=3, sticky=NSEW)
        auto_button.grid(row=2, column=2, columnspan=3, sticky=NSEW)
        manual_button.grid(row=2, column=5, columnspan=3, sticky=NSEW)
        pages.pack(expand=True, fill=BOTH)

    def place(self, widget: Widget, x, y):
        widget.place(x=(x / 100.0 * self.win_dimension.width - widget.winfo_width() / 2),
                     y=(y / 100.0 * self.win_dimension.height - widget.winfo_height()))

    @staticmethod
    def _add_page(pages: ttk.Notebook, page: Frame, title: str):
        page.pack(fill=BOTH, expand=True)
        pages.add(page, text=title)
        return page


