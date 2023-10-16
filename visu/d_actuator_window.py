from tkinter import ttk

from rx.subject import Subject

import di_conf.container as DI
from services.d_actuator_plc_service import DActuatorPLCService
from utils.checkbox_lines import CheckBoxList, CheckBoxLine
from utils.frame_canvas import FrameCanvas
from utils.input_textfield import InputTextField
from utils.structures import Dimension, ValueWithChangeFlag, StateColor, TextFieldPars
from tkinter import *

from visu.dialog import ConfirmDialog, InfoDialog
from visu.status_bar import statusBar


class DActuatorWindow(Toplevel):
    def __init__(self, name: str, parent):
        self.sc = DI.Container.screen_creator()
        self.da_pars = DI.Container.da_pars()
        self.common = DI.Container.common()
        self.win_dimension = Dimension(400, 300)
        super().__init__(self.sc._main_frame)
        self.status_img = parent.status_imgs
        self.plc_data: DActuatorPLCService = parent.plc_data
        self.status_texts = self.da_pars.text_status(name)

        self.title(name)
        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())
        self.resizable(False, False)
        self.popup()
        self.pages_frame = Frame(self)
        self.status_bar = statusBar(self, name, lambda e: self._toggle_da(var=self.plc_data.err_reset, value=True))

        self.pages = ttk.Notebook(self.pages_frame, height=self.win_dimension.height - 55)
        self.page1 = self._add_page(self.pages, Frame(self.pages), "Управление")
        self.page2 = self._add_page(self.pages, Frame(self.pages), "Блокировки")
        self.page3 = self._add_page(self.pages, Frame(self.pages), "Автостарт")
        self.page4 = self._add_page(self.pages, Frame(self.pages), "Автостоп")
        self.page5 = self._add_page(self.pages, Frame(self.pages), "Ошибки")
        self.page6 = self._add_page(self.pages, Frame(self.pages), "Сервис")

        self.status_picture = FrameCanvas(self.page1, self.status_img[0])
        self.start_button = Button(self.page1, text=self.da_pars.text_start(name),
                                   command=lambda:
                                   ConfirmDialog(self, lambda: self._toggle_da(var=self.plc_data.start, value=True),
                                                 text=f'Подтвердить "{self.da_pars.text_start(name)}"?'))
        self.stop_button = Button(self.page1, text=self.da_pars.text_stop(name),
                                  command=lambda:
                                  ConfirmDialog(self, lambda: self._toggle_da(var=self.plc_data.start, value=False),
                                                text=f'Подтвердить "{self.da_pars.text_stop(name)}"?'))
        self.auto_button = Button(self.page1, text='Автомат',
                                  command=lambda:
                                  ConfirmDialog(self, lambda: self._toggle_da(var=self.plc_data.auto, value=True),
                                                text='Переключить в автоматический режим?'))
        self.manual_button = Button(self.page1, text='Ручной',
                                    command=lambda:
                                    ConfirmDialog(self, lambda: self._toggle_da(var=self.plc_data.auto, value=False),
                                                  text='Переключить в ручной режим?'))
        self.model_check_box = CheckBoxLine(self.page6, 'Моделирование', StateColor(active='yellow'),
                                            apply_action=lambda value: self._toggle_da(var=self.plc_data.modeling,
                                                                                       value=value))

        for i in range(10):
            self.page1.grid_columnconfigure(i, minsize=self.win_dimension.width / 10)

        self.status_picture.grid(row=0, column=3, columnspan=4, sticky=NSEW)
        self.start_button.grid(row=1, column=2, columnspan=3, sticky=NSEW)
        self.stop_button.grid(row=1, column=5, columnspan=3, sticky=NSEW)
        self.auto_button.grid(row=2, column=2, columnspan=3, sticky=NSEW)
        self.manual_button.grid(row=2, column=5, columnspan=3, sticky=NSEW)

        self.lock_list = self._get_check_box_list(self.page2, self.plc_data.locks_mask,
                                                  'Блокировки:',
                                                  self.da_pars.text_lock(name),
                                                  colors=StateColor(active='yellow'))

        self.start_list = self._get_check_box_list(self.page3, self.plc_data.auto_start_mask,
                                                   'Условия автоматического старта:',
                                                   self.da_pars.text_auto_start(name),
                                                   colors=StateColor(active='green'))

        self.stop_list = self._get_check_box_list(self.page4, self.plc_data.auto_stop_mask,
                                                  'Условия автоматической остановки:',
                                                  self.da_pars.text_auto_stop(name),
                                                  colors=StateColor(active='green'))

        self.errors_list = self._get_check_box_list(self.page5, self.plc_data.errors_mask,
                                                    'Ошибки:',
                                                    self.da_pars.text_errors(name))
        self.input_fb_on_delay = self._get_input_field(self.page6, self.plc_data.fb_on_err_delay,
                                                       'Задержка включения:', TextFieldPars(up_lim=65535, dec_place=0))
        self.input_fb_off_delay = self._get_input_field(self.page6, self.plc_data.fb_off_err_delay,
                                                        'Задержка выключения:',
                                                        TextFieldPars(up_lim=65535, dec_place=0))
        self.input_fb_on_delay.pack(side=TOP, fill=BOTH)
        self.input_fb_off_delay.pack(side=TOP, fill=BOTH)
        self.model_check_box.pack(side=TOP, fill=BOTH)
        self.pages.pack(fill=BOTH, expand=True)
        self.pages_frame.grid(row=0, sticky=EW)
        self.status_bar.grid(row=1, sticky=EW)

    @staticmethod
    def _add_page(pages: ttk.Notebook, page: Frame, title: str):
        page.pack(fill=BOTH, expand=True)
        pages.add(page, text=title)
        return page

    def _get_check_box_list(self, parent, mask_var, header_text, texts_for_lines, colors=StateColor()) -> CheckBoxList:
        subject = Subject()
        subject.subscribe(lambda value: self.set_mask(mask_var=mask_var, value=value))
        check_box_list = CheckBoxList(parent, header_text, texts_for_lines, subject, colors)
        check_box_list.pack(side=TOP, fill=BOTH)
        return check_box_list

    def _get_input_field(self, parent, delay_var, text_label, text_pars: TextFieldPars) -> InputTextField:
        subject = Subject()
        subject.subscribe(lambda value: self.set_fb_delay(delay_var=delay_var, value=value))
        return InputTextField(parent, text_label, subject, text_pars)

    def popup(self):
        self.deiconify()
        self.focus_set()
        self.attributes("-topmost", True)
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

        self.status_bar.change_visu(par)
        match par.name:
            case 'status':
                self.status_picture.new_image(self.status_img[par.get()])
            case 'locks':
                self.lock_list.set_status(self.plc_data.locks.get())
            case 'locks_mask':
                self.lock_list.set_mask(self.plc_data.locks_mask.get())
            case 'auto_start':
                self.start_list.set_status(self.plc_data.auto_start.get())
            case 'auto_start_mask':
                self.start_list.set_mask(self.plc_data.auto_start_mask.get())
            case 'auto_stop':
                self.stop_list.set_status(self.plc_data.auto_stop.get())
            case 'auto_stop_mask':
                self.stop_list.set_mask(self.plc_data.auto_stop_mask.get())
            case 'errors':
                self.errors_list.set_status(self.plc_data.errors.get())
            case 'errors_mask':
                self.errors_list.set_mask(self.plc_data.errors_mask.get())
            case 'fb_on_err_delay':
                self.input_fb_on_delay.set_current_value(self.plc_data.fb_on_err_delay.get())
            case 'fb_off_err_delay':
                self.input_fb_off_delay.set_current_value(self.plc_data.fb_off_err_delay.get())
            case 'modeling':
                self.model_check_box.set_attributes(self.plc_data.modeling.get())

    @staticmethod
    def send_decor(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            func(self, **kwargs)
            self.plc_data.send()

        return wrapper

    @send_decor
    def _toggle_da(self, var, value=False):
        var.set(value)

    @send_decor
    def set_mask(self, mask_var: ValueWithChangeFlag, value: int):
        mask_var.set(value)

    @send_decor
    def set_fb_delay(self, delay_var: ValueWithChangeFlag, value: int):
        delay_var.set(value)
