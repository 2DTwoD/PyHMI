from tkinter import Frame, Button, LEFT

from services.common_service import CommonService
from utils.frame_canvas import FrameCanvas
from utils.frame_label import FrameLabel

import di_conf.container as DI
from utils.structures import ValueWithChangeFlag, Dimension


class StatusBar(Frame):
    def __init__(self, parent, dimension: Dimension = Dimension(0, 0)):
        super(StatusBar, self).__init__(parent)
        self.common = DI.Container.common()
        self.da_pars = DI.Container.da_pars()
        self.alarm_tokens = [self.common.get_token(CommonService.NO_ALARM, dimension),
                             self.common.get_token(CommonService.ALARM, dimension)]
        self.lock_tokens = [self.common.get_token(CommonService.UNLOCKED, dimension),
                            self.common.get_token(CommonService.LOCKED, dimension)]
        self.service_tokens = [self.common.get_token(CommonService.NO_SERVICE, dimension),
                               self.common.get_token(CommonService.SERVICE, dimension)]
        self.alarm_token = FrameCanvas(self, self.alarm_tokens[0])
        self.lock_token = FrameCanvas(self, self.lock_tokens[0])
        self.service_token = FrameCanvas(self, self.service_tokens[0])
        self.auto_token = FrameLabel(self, text='А', bg='green', fg='white', dimension=dimension)

    def change_visu(self, par: ValueWithChangeFlag):
        match par.name:
            case 'auto':
                (text, bg, fg) = ('А', 'green', 'white') if par.get() else ('Р', 'yellow', 'red')
                self.auto_token.config_label(text=text, background=bg, foreground=fg)
            case 'alarm':
                self.alarm_token.new_image(self.alarm_tokens[par.get()])
            case 'locked':
                self.lock_token.new_image(self.lock_tokens[par.get()])
            case 'service':
                self.service_token.new_image(self.service_tokens[par.get()])


class WindowStatusBar(StatusBar):
    def __init__(self, parent, name: str, reset_errors_action):
        super(WindowStatusBar, self).__init__(parent)
        self.status_texts = self.da_pars.text_status(name)
        self.status_text = FrameLabel(self, dimension=Dimension(100, 25))
        self.err_reset_button = Button(self, text='Сброс аварий')
        self.err_reset_button.bind('<Button-1>', reset_errors_action)

        self.err_reset_button.pack(side=LEFT)
        self.alarm_token.pack(side=LEFT)
        self.lock_token.pack(side=LEFT)
        self.service_token.pack(side=LEFT)
        self.auto_token.pack(side=LEFT)
        self.status_text.pack(side=LEFT)

    def change_visu(self, par: ValueWithChangeFlag):
        if par.name == 'status':
            self.status_text.config_label(text=self.status_texts[par.get()])
        super(WindowStatusBar, self).change_visu(par)


class StatusBarType1(StatusBar):
    def __init__(self, parent, img_dimension: Dimension):
        super(StatusBarType1, self).__init__(parent, img_dimension)
        self.img_dimension = img_dimension
        self.alarm_token.pack(side=LEFT)
        self.lock_token.pack(side=LEFT)
        self.service_token.pack(side=LEFT)
        self.auto_token.pack(side=LEFT)

    def width(self):
        return int(self.img_dimension.width * 4)
