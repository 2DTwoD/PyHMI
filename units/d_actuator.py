from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk
import di_conf.container as DI
from services.d_actuator_service import DActuatorService
from utils.frame_canvas import FrameCanvas
from utils.structures import NameImage, Coordinate, Area, Dimension


class DActuator:
    def __init__(self, name, parameters):
        self.sc = DI.Container.screen_creator()
        self.name = name
        picture_tag = name + "_status"
        self.stop_img = NameImage(name=picture_tag, image=ImageTk.PhotoImage(Image.open(parameters.img_path.stop)))
        self.start_img = NameImage(name=picture_tag, image=ImageTk.PhotoImage(Image.open(parameters.img_path.start)))
        self.intermed_img = NameImage(name=picture_tag, image=ImageTk.PhotoImage(Image.open(parameters.img_path.stop)))
        self.alarm_img = NameImage(name=picture_tag, image=ImageTk.PhotoImage(Image.open(parameters.img_path.alarm)))
        self.alarm_token = NameImage(name="alarm_token",
                                     image=ImageTk.PhotoImage(Image.open('res/pics/common/alarm.png')))

        self.location = {}
        for screen_name, location in parameters.location.__dict__.items():
            self.location[screen_name] = Coordinate(location.x, location.y)
        self.win_dimension = Dimension(300, 200)
        self.current_img = self.stop_img
        self.image_dimension = Dimension(max(self.stop_img.width(), self.start_img.width(), self.alarm_img.width()),
                                         max(self.stop_img.height(), self.start_img.height(), self.alarm_img.height()))
        self.plc_data = DActuatorService(parameters.start_address, parameters.start_address + 7)
        self.click_area = Area()
        self.window = None

        self._create_widgets()

        self.change_screen()

    def update(self):
        self.plc_data.update()
        match(self.plc_data.status):
            case 0:
                self.current_img = self.stop_img
            case 1:
                self.current_img = self.start_img
            case 2:
                self.current_img = self.intermed_img
            case _:
                self.current_img = self.alarm_img
        self._update_pic(self.current_img)

        # print(self.plc_data)

    def change_screen(self):
        if self.sc.current_screen in self.location:
            x = self.location[self.sc.current_screen].x
            y = self.location[self.sc.current_screen].y
            self.sc.screen_add_image(x, y, self.current_img)
            self.click_area.update(y - self.image_dimension.height / 2, y + self.image_dimension.height / 2,
                                   x - self.image_dimension.width / 2, x + self.image_dimension.width / 2)

    def close_window(self):
        self.window.destroy()
        self.window = None

    def left_click(self, mouse_x, mouse_y):
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

    @staticmethod
    def _add_page(pages: ttk.Notebook, page: Frame, title: str):
        page.pack(fill=BOTH, expand=True)
        pages.add(page, text=title)
        return page

    def _update_pic(self, img: NameImage):
        if self.window is not None:
            self.status_picture.new_image(img)
        if self.sc.current_screen in self.location:
            self.sc.screen_add_image(self.location[self.sc.current_screen].x, self.location[self.sc.current_screen].y, img)

    def _create_widgets(self):
        self.pages_frame = Frame(self.window)
        self.status_frame = Frame(self.window)

        self.pages = ttk.Notebook(self.pages_frame, height=self.win_dimension.height - 55)
        self.page1 = self._add_page(self.pages, ttk.Frame(self.pages), "Control")
        self.page2 = self._add_page(self.pages, ttk.Frame(self.pages), "Locks")
        self.page3 = self._add_page(self.pages, ttk.Frame(self.pages), "Auto conditions")
        self.page4 = self._add_page(self.pages, ttk.Frame(self.pages), "Errors")
        self.page5 = self._add_page(self.pages, ttk.Frame(self.pages), "Service")

        self.alarm_token = FrameCanvas(self.status_frame, self.alarm_token)
        self.status_picture = FrameCanvas(self.page1, self.current_img)
        self.start_button = Button(self.page1, text='Старт')
        self.stop_button = Button(self.page1, text='Стоп')
        self.auto_button = Button(self.page1, text='Автомат')
        self.manual_button = Button(self.page1, text='Ручной')

        # def click(event):
        #     self.sc.screen_add_image(self.location[self.sc.current_screen].x,
        #                              self.location[self.sc.current_screen].y,
        #                              self.start_img)
        #
        # start_button.bind('<Button-1>', click)
        for i in range(10):
            self.page1.grid_columnconfigure(i, minsize=self.win_dimension.width / 10)
        self.status_picture.grid(row=0, column=3, columnspan=4, sticky=NSEW)
        self.start_button.grid(row=1, column=2, columnspan=3, sticky=NSEW)
        self.stop_button.grid(row=1, column=5, columnspan=3, sticky=NSEW)
        self.auto_button.grid(row=2, column=2, columnspan=3, sticky=NSEW)
        self.manual_button.grid(row=2, column=5, columnspan=3, sticky=NSEW)

        self.pages.pack()
        self.alarm_token.pack()
        self.pages_frame.grid(row=0)
        self.status_frame.grid(row=1, sticky=W)
