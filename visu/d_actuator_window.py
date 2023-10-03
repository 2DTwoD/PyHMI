from tkinter import ttk
import di_conf.container as DI
from services.d_actuator_plc_service import DActuatorPLCService
from utils.frame_canvas import FrameCanvas
from utils.structures import Dimension
from tkinter import *


class DActuatorWindow(Toplevel):
    def __init__(self, name: str, parent):
        self.sc = DI.Container.screen_creator()
        self.da_pars = DI.Container.da_pars()
        self.common = DI.Container.common()
        self.win_dimension = Dimension(300, 200)
        super().__init__(self.sc._main_frame)
        self.status_img = parent.status_imgs
        self.alarm_tokens = parent.alarm_tokens
        self.service_tokens = parent.service_tokens
        self.lock_tokens = parent.lock_tokens
        self.plc_data: DActuatorPLCService = parent.plc_data

        self.title(name)
        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())
        self.attributes("-topmost", True)
        self.resizable(False, False)
        self.popup()
        self.pages_frame = Frame(self)
        self.status_frame = Frame(self)

        self.pages = ttk.Notebook(self.pages_frame, height=self.win_dimension.height - 55)
        self.page1 = self._add_page(self.pages, ttk.Frame(self.pages), "Control")
        self.page2 = self._add_page(self.pages, ttk.Frame(self.pages), "Locks")
        self.page3 = self._add_page(self.pages, ttk.Frame(self.pages), "Auto conditions")
        self.page4 = self._add_page(self.pages, ttk.Frame(self.pages), "Errors")
        self.page5 = self._add_page(self.pages, ttk.Frame(self.pages), "Service")

        self.alarm_token = FrameCanvas(self.status_frame, self.alarm_tokens[0])
        self.status_picture = FrameCanvas(self.page1, self.status_img[0])
        self.start_button = Button(self.page1, text='Старт')
        self.stop_button = Button(self.page1, text='Стоп')
        self.auto_button = Button(self.page1, text='Автомат')
        self.manual_button = Button(self.page1, text='Ручной')

        self.start_button.bind('<Button-1>', self._start_da)
        self.stop_button.bind('<Button-1>', self._stop_da)

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

        self.set_status(parent.plc_data.status.get())

    @staticmethod
    def _add_page(pages: ttk.Notebook, page: Frame, title: str):
        page.pack(fill=BOTH, expand=True)
        pages.add(page, text=title)
        return page

    def popup(self):
        self.deiconify()
        self.focus_set()
        root_mouse = self.sc.get_root_mouse_position()
        self.geometry(f"{self.win_dimension.width}x{self.win_dimension.height}+{root_mouse.x}+{root_mouse.y}")

    def set_status(self, status):
        self.status_picture.new_image(self.status_img[status])

    @staticmethod
    def send_decor(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            func(self)
            self.plc_data.send()
        return wrapper

    @send_decor
    def _start_da(self):
        self.plc_data.start.set(True)
        self.plc_data.fb_on_err_delay.set(200)

    @send_decor
    def _stop_da(self):
        self.plc_data.start.set(False)

