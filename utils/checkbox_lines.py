from tkinter import Frame, Canvas, LEFT, RIGHT, Checkbutton, BOTH, TOP, BooleanVar, Button, E, W, Label
from tkinter.font import Font

from rx.subject import Subject

from utils.structures import StateColor


class CheckBoxList(Frame):
    def __init__(self, parent, header_text: str, texts: tuple, subject: Subject, colors: StateColor):
        super().__init__(parent)
        self.check_box_lines = []
        self.mask = 0
        self.page_header = Frame(self)
        self.colors = colors
        Label(self.page_header, text=header_text, anchor=W).pack(side=LEFT)
        Label(self.page_header, text='Выкл.', anchor=E).pack(side=RIGHT)
        self.page_header.pack(side=TOP, fill=BOTH)
        for index, text in enumerate(texts):
            if index > 7:
                break
            line = CheckBoxLine(self, text, index)
            line.pack(side=TOP, fill=BOTH)
            self.check_box_lines.append(line)

        def apply_action():
            subject.on_next(self.mask)
            self.apply_button.config(background='gray94')
            self._set_apply_color()

        self.apply_button = Button(self, text='Применить', command=apply_action)
        self.apply_button.pack(side=TOP, anchor=E)

    def set_mask(self, value: int):
        self.mask = value
        for index, line in enumerate(self.check_box_lines):
            line.set_check_box(value & (1 << index))

    def set_status(self, value: int):
        for index, line in enumerate(self.check_box_lines):
            line.set_rect_color(value & (1 << index), self.colors)

    def _set_apply_color(self):
        for index, line in enumerate(self.check_box_lines):
            line.set_check_box_color('white')

    def prep_mask(self, value):
        self.apply_button.config(background='cyan')
        self.mask ^= value


class CheckBoxLine(Frame):
    def __init__(self, parent: CheckBoxList, text: str, shift: int):
        super().__init__(parent)
        self._selected = BooleanVar()

        def click_action():
            parent.prep_mask(1 << shift)
            self.set_check_box_color('cyan')

        self.font = Font(size=8, overstrike=False)
        self._check_box = Checkbutton(self, command=click_action, variable=self._selected, selectcolor='white')
        self._label = Label(self, text=text, font=self.font)
        self._rect_canvas = Canvas(self, width=20, height=20, highlightthickness=0)
        self._rect = self._rect_canvas.create_rectangle(0, 0, 20, 20, fill='gray')
        self._rect_canvas.place(x=0, y=0)
        self._rect_canvas.pack(side=LEFT)
        self._label.pack(side=LEFT)
        self._check_box.pack(side=RIGHT)

    def set_check_box(self, value: int):
        self._selected.set(value > 0)
        self.font.config(overstrike=value > 0)

    def set_rect_color(self, value: int, colors: StateColor):
        self._rect_canvas.itemconfig(self._rect, fill=colors.active if value > 0 else colors.no_active)

    def set_check_box_color(self, color: str):
        self._check_box.config(selectcolor=color)
