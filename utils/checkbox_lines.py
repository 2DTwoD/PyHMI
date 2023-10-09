from tkinter import Frame, Canvas, LEFT, RIGHT, Checkbutton, BOTH, TOP, BooleanVar, Button, E, W
from tkinter.ttk import Label

from rx.subject import Subject


class CheckBoxList(Frame):
    def __init__(self, parent, header_text: str, texts: tuple, subject: Subject):
        super().__init__(parent)
        self.check_box_lines = []
        self.mask = 0
        self.page_header = Frame(self)
        Label(self.page_header, text=header_text, anchor=W).pack(side=LEFT)
        Label(self.page_header, text='Выкл.', anchor=E).pack(side=RIGHT)
        self.page_header.pack(side=TOP, fill=BOTH)
        for index, text in enumerate(texts):
            if index > 7:
                break
            line = CheckBoxLine(self, text, index)
            line.pack(side=TOP, fill=BOTH)
            self.check_box_lines.append(line)
        self.apply_button = Button(self, text='Применить', command=lambda: subject.on_next(self.mask))
        self.apply_button.pack(side=TOP, anchor=E)

    def set_mask(self, value: int):
        self.mask = value
        for index, line in enumerate(self.check_box_lines):
            line.set_check_box(value & (1 << index))

    def prep_mask(self, value):
        self.mask ^= value


class CheckBoxLine(Frame):
    def __init__(self, parent: CheckBoxList, text: str, shift: int):
        super().__init__(parent)
        self._selected = BooleanVar()
        self._check_box = Checkbutton(self, command=lambda: parent.prep_mask(1 << shift), variable=self._selected)
        self._label = Label(self, text=text)
        self._rect_canvas = Canvas(self, width=20, height=20, highlightthickness=0)
        self._rect = self._rect_canvas.create_rectangle(0, 0, 20, 20, fill='gray')
        self._rect_canvas.place(x=0, y=0)
        self._rect_canvas.pack(side=LEFT)
        self._label.pack(side=LEFT)
        self._check_box.pack(side=RIGHT)

    def set_check_box(self, value: int):
        self._selected.set(value > 0)
