from tkinter import ttk

from rx.subject import Subject

import di_conf.container as DI
from services.d_actuator_plc_service import DActuatorPLCService
from utils.checkbox_lines import CheckBoxList
from utils.frame_canvas import FrameCanvas
from utils.frame_label import FrameLabel
from utils.structures import Dimension, ValueWithChangeFlag
from tkinter import *



class DActuatorWindow(Toplevel):
    def __init__(self, name: str, parent):
        self.sc = DI.Container.screen_creator()
        self.da_pars = DI.Container.da_pars()
        self.common = DI.Container.common()
        self.win_dimension = Dimension(300, 280)
        super().__init__(self.sc._main_frame)
        self.status_img = parent.status_imgs
        self.alarm_tokens = parent.alarm_tokens
        self.service_tokens = parent.service_tokens
        self.lock_tokens = parent.lock_tokens
        self.service_token = parent.service_tokens
        self.plc_data: DActuatorPLCService = parent.plc_data
        self.status_texts = self.da_pars.text_status(name)

        self.title(name)
        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())
        self.attributes("-topmost", True)
        self.resizable(False, False)
        self.popup()
        self.pages_frame = Frame(self)
        self.status_frame = Frame(self)

        self.pages = ttk.Notebook(self.pages_frame, height=self.win_dimension.height - 55)
        self.page1 = self._add_page(self.pages, Frame(self.pages), "Control")
        self.page2 = self._add_page(self.pages, Frame(self.pages), "Locks")
        self.page3 = self._add_page(self.pages, Frame(self.pages), "Auto conditions")
        self.page4 = self._add_page(self.pages, Frame(self.pages), "Errors")
        self.page5 = self._add_page(self.pages, Frame(self.pages), "Service")

        self.alarm_token = FrameCanvas(self.status_frame, self.alarm_tokens[0])
        self.lock_token = FrameCanvas(self.status_frame, self.lock_tokens[0])
        self.service_token = FrameCanvas(self.status_frame, self.service_tokens[0])
        self.auto_token = FrameLabel(self.status_frame, text='A', bg='green', fg='white', width=25, height=25)
        self.status_text = FrameLabel(self.status_frame, width=100)
        self.status_picture = FrameCanvas(self.page1, self.status_img[0])
        self.start_button = Button(self.page1, text=self.da_pars.text_start(name))
        self.stop_button = Button(self.page1, text=self.da_pars.text_stop(name))
        self.auto_button = Button(self.page1, text='Автомат')
        self.manual_button = Button(self.page1, text='Ручной')
        self.err_reset_button = Button(self.status_frame, text='Сброс аварий')

        self.start_button.bind('<Button-1>', lambda e: self._start_da(value=True))
        self.stop_button.bind('<Button-1>', lambda e: self._start_da(value=False))
        self.auto_button.bind('<Button-1>', lambda e: self._auto_da(value=True))
        self.manual_button.bind('<Button-1>', lambda e: self._auto_da(value=False))
        self.err_reset_button.bind('<Button-1>', self._reset_errors)

        for i in range(10):
            self.page1.grid_columnconfigure(i, minsize=self.win_dimension.width / 10)

        self.status_picture.grid(row=0, column=3, columnspan=4, sticky=NSEW)
        self.start_button.grid(row=1, column=2, columnspan=3, sticky=NSEW)
        self.stop_button.grid(row=1, column=5, columnspan=3, sticky=NSEW)
        self.auto_button.grid(row=2, column=2, columnspan=3, sticky=NSEW)
        self.manual_button.grid(row=2, column=5, columnspan=3, sticky=NSEW)

        self.lock_subject = Subject()
        self.lock_subject.subscribe(lambda value: self.set_locks_mask(mask_var=self.plc_data.locks_mask, value=value))
        self.page2_header = Frame(self.page2)
        self.lock_list = CheckBoxList(self.page2, self.da_pars.text_lock(name), self.lock_subject)
        Label(self.page2_header, text='Условия автоматического старта:', anchor=W).pack(side=LEFT)
        Label(self.page2_header, text='Выкл.', anchor=E).pack(side=RIGHT)
        self.page2_header.pack(side=TOP, fill=BOTH)
        self.lock_list.pack(side=TOP, fill=BOTH)

        self.err_reset_button.pack(side=LEFT)
        self.alarm_token.pack(side=LEFT)
        self.lock_token.pack(side=LEFT)
        self.service_token.pack(side=LEFT)
        self.auto_token.pack(side=LEFT)
        self.status_text.pack(side=LEFT)
        self.pages.pack(fill=BOTH, expand=True)
        self.pages_frame.grid(row=0, sticky=EW)
        self.status_frame.grid(row=1, sticky=EW)


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

    def change_visu(self, par: ValueWithChangeFlag):
        self.auto_button['state'] = 'disabled' if self.plc_data.auto.get() else 'normal'
        self.manual_button['state'] = 'normal' if self.plc_data.auto.get() else 'disabled'
        if self.plc_data.auto.get():
            self.start_button['state'] = 'disabled'
            self.stop_button['state'] = 'disabled'
        else:
            self.start_button['state'] = 'disabled' if self.plc_data.start.get() else 'normal'
            self.stop_button['state'] = 'normal' if self.plc_data.start.get() else 'disabled'

        match par.name:
            case 'status':
                self.status_picture.new_image(self.status_img[par.get()])
                self.status_text.config_label(text=self.status_texts[par.get()])
            case 'auto':
                (text, bg, fg) = ('A', 'green', 'white') if par.get() else ('M', 'yellow', 'red')
                self.auto_token.config_label(text=text, background=bg, foreground=fg)
            case 'alarm':
                self.alarm_token.new_image(self.alarm_tokens[par.get()])
            case 'locked':
                self.lock_token.new_image(self.lock_tokens[par.get()])
            case 'service':
                self.service_token.new_image(self.service_tokens[par.get()])
            case 'locks_mask':
                self.lock_list.set_mask(self.plc_data.locks_mask.get())

    @staticmethod
    def send_decor(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            func(self, **kwargs)
            self.plc_data.send()
        return wrapper

    @send_decor
    def _start_da(self, value=False):
        self.plc_data.start.set(value)

    @send_decor
    def _auto_da(self, value=False):
        self.plc_data.auto.set(value)
        self.plc_data.auto_start_mask.set(0)
        self.plc_data.auto_stop_mask.set(0)
        self.plc_data.locks_mask.set(0)
        self.plc_data.errors_mask.set(0)

    @send_decor
    def _reset_errors(self):
        self.plc_data.err_reset.set(True)

    @send_decor
    def set_locks_mask(self, mask_var: ValueWithChangeFlag, value: int):
        mask_var.set(mask_var.get() ^ value)

