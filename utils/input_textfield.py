from tkinter import Frame, Entry, Label, LEFT, Button, RIGHT, W, StringVar

from rx.subject import Subject

from utils.structures import TextFieldPars


class InputTextField(Frame):
    def __init__(self, parent, text: str, subject: Subject, pars: TextFieldPars = TextFieldPars()):
        super().__init__(parent)
        self.pars = pars
        self._input_text = StringVar()
        self._label = Label(self, text=text)
        self._current_value = Label(self, width=pars.width, text=0, anchor=W)
        self._entry = Entry(self, width=pars.width, validate="all", textvariable=self._input_text)
        self._button = Button(self, text='Применить', command=lambda: self.apply(subject))

        self._entry.bind('<KeyRelease>', lambda e: self.check_entry())
        self._label.pack(side=LEFT)
        self._current_value.pack(side=LEFT)
        self._button.pack(side=RIGHT)
        self._entry.pack(side=RIGHT)

    def check_entry(self):
        input_val = ''
        dot_flag = True
        for c in self._entry.get():
            if c in '1234567890':
                input_val += c
            if c in '.,' and dot_flag:
                input_val += c
                dot_flag = False
        if len(input_val) > self.pars.width:
            input_val = input_val[:-1]
        self._input_text.set(input_val)


    def apply(self, subject):
        if self.pars.numeric:
            try:
                entry_value = float(self._entry.get().replace(',', '.'))
            except:
                print('Введнное число не корректно')
                return
            entry_value = max(min(self.pars.up_lim, entry_value), self.pars.down_lim)
            entry_value = round(entry_value, self.pars.dec_place)
            subject.on_next(entry_value)
        else:
            subject.on_next(self._entry.get())

    def set_current_value(self, value):
        self._current_value.config(text=str(value))
