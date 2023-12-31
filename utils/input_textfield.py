from tkinter import Frame, Entry, Label, LEFT, Button, RIGHT, W, StringVar
import re

from utils.structures import TextFieldPars
from visu.dialog import InfoDialog, ConfirmDialog


class InputTextField(Frame):
    def __init__(self, parent, text: str, apply_action, pars: TextFieldPars = TextFieldPars()):
        super().__init__(parent)
        self._pars = pars
        self._input_text = StringVar()
        self._input_text.trace("w", self.check_entry)
        self._label = Label(self, text=text)
        self._current_value = Label(self, width=pars.width, text=0, anchor=W)
        self._entry = Entry(self, width=pars.width, validate="all", textvariable=self._input_text)
        self._button = Button(self,
                              text='Применить',
                              command=lambda: ConfirmDialog(parent, lambda: self.apply(apply_action),
                              text=f'Применить значение "{self._input_text.get()}"?'))

        self._label.pack(side=LEFT)
        self._current_value.pack(side=LEFT)
        self._button.pack(side=RIGHT)
        self._entry.pack(side=RIGHT)

    def check_entry(self, *args):
        pattern = re.compile("-?\d*(\.?|,?)\d*")
        if not pattern.fullmatch(self._input_text.get()) or len(self._input_text.get()) > self._pars.width:
            self._input_text.set(self._input_text.get()[:-1])
            return
        self._entry.config(background='cyan')

    def apply(self, apply_action):
        if self._pars.numeric:
            try:
                entry_value = float(self._entry.get().replace(',', '.'))
            except:
                InfoDialog(self, 'Введенное число не корректно', mode=InfoDialog.WARNING)
                return
            if entry_value > self._pars.up_lim or entry_value < self._pars.down_lim:
                InfoDialog(self,
                           f'Введенное число должно быть в пределах от {self._pars.down_lim} до {self._pars.up_lim}',
                           mode=InfoDialog.WARNING)
            entry_value = max(min(self._pars.up_lim, entry_value), self._pars.down_lim)
            if self._pars.dec_place > 0:
                entry_value = round(entry_value, self._pars.dec_place)
            else:
                entry_value = int(entry_value)
            apply_action(entry_value)
            self._input_text.set(str(entry_value))
        else:
            apply_action(self._entry.get())
        self._entry.config(background='white')

    def set_current_value(self, value):
        self._current_value.config(text=str(value))
