from tkinter import Frame, Canvas, LEFT, RIGHT, Checkbutton, BOTH, TOP
from tkinter.ttk import Label

from rx.subject import Subject


class CheckBoxList(Frame):
    def __init__(self, parent, texts: tuple, subject: Subject):
        super().__init__(parent)
        self.lock_lines = []
        for index, text in enumerate(texts):
            if index > 7:
                break
            line = CheckBoxLine(self, text, index, subject)
            line.pack(side=TOP, fill=BOTH)
            self.lock_lines.append(line)

    def set_mask(self, value: int):
        for index, line in enumerate(self.lock_lines):
            line.set_check_box(value & (1 << index))


class CheckBoxLine(Frame):
    def __init__(self, parent, text: str, shift: int, subject: Subject):
        super().__init__(parent)
        self._choosen = False
        self._check_box = Checkbutton(self, command=lambda: subject.on_next(1 << shift), onvalue=self._choosen,
                                      offvalue=self._choosen)
        self._label = Label(self, text=text)
        self._rect_canvas = Canvas(self, width=20, height=20, highlightthickness=0)
        self._rect = self._rect_canvas.create_rectangle(0, 0, 20, 20, fill='gray')
        self._rect_canvas.place(x=0, y=0)
        self._rect_canvas.pack(side=LEFT)
        self._label.pack(side=LEFT)
        self._check_box.pack(side=RIGHT)

    def set_check_box(self, value: int):
        self._choosen = 1 if value > 0 else 0
        # if value > 0:
        #     self._check_box.select()
        # else:
        #     self._check_box.deselect()
