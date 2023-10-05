from tkinter import Frame, Label, BOTH
from tkinter import Widget


class FrameLabel(Frame):
    def __init__(self, parent: Widget, width: int = 25, height: int = 25, text: str = '0', bg: str = 'white', fg: str = 'black'):
        super().__init__(parent, width=width, height=height)
        self.pack_propagate(0)
        self.label = Label(self, text=text, background=bg, foreground=fg)
        self.label.pack(fill=BOTH, expand=1)

    def config_label(self, **kwargs):
        self.label.config(**kwargs)
