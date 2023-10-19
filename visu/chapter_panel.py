from tkinter import Frame, BaseWidget, Button
import di_conf.container as DI


class ChapterPanel(Frame):
    def __init__(self, parent: BaseWidget):
        super(ChapterPanel, self).__init__(parent)
        _main_pars = DI.Container.main_pars()
        self._button_list = []
        for screen_name in _main_pars.screens:
            button = Button(self, text=screen_name)
            self._button_list.append(button)
            button.grid()

