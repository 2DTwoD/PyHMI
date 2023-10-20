from tkinter import Frame, BaseWidget, Label, LEFT, Button, RIGHT
from time import strftime
import di_conf.container as DI


class FooterPanel(Frame):
    def __init__(self, parent: BaseWidget):
        super(FooterPanel, self).__init__(parent)
        self._sc = DI.Container.screen_creator()
        self._clock = Label(self)
        self._exit_button = Button(self, text='Выход', command=self._sc.exit)
        self.tick()
        self._clock.pack(side=LEFT)
        self._exit_button.pack(side=RIGHT)

    def tick(self):
        self._clock.config(text=strftime('%H:%M:%S\n%d.%m.%Y'))
        self._clock.after(1000, self.tick)
