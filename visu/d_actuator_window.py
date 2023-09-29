from tkinter import Toplevel, Frame, ttk, Button
import di_conf.container as DI
from utils.frame_canvas import FrameCanvas


class DActuatorWindow(Toplevel):
    def __init__(self, name: str):
        self.sc = DI.Container.screen_creator()
        super().__init__(self.sc.main_frame)
        self.title(name)
        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())
        self.attributes("-topmost", True)
        self.resizable(False, False)
        self.pages_frame = Frame(self)
        self.status_frame = Frame(self)

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

    @staticmethod
    def _add_page(pages: ttk.Notebook, page: Frame, title: str):
        page.pack(fill=BOTH, expand=True)
        pages.add(page, text=title)
        return page