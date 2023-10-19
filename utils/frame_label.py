from tkinter import Frame, Label, BOTH
from tkinter import Widget

from utils.structures import Dimension


class FrameLabel(Frame):
    DEFAULT_DIM = Dimension(25, 25)

    def __init__(self, parent: Widget, dimension: Dimension = DEFAULT_DIM, text: str = '0', bg: str = 'white', fg: str = 'black'):
        if dimension.isZero():
            dimension = FrameLabel.DEFAULT_DIM
        super().__init__(parent, width=dimension.width, height=dimension.height)
        self.pack_propagate(0)
        self.label = Label(self, text=text, background=bg, foreground=fg)
        self.label.pack(fill=BOTH, expand=1)

    def config_label(self, **kwargs):
        self.label.config(**kwargs)

