from tkinter import Frame, Canvas, W

from utils.structures import NameImage


class FrameCanvas(Frame):
    def __init__(self, master, name_image: NameImage):
        super().__init__(master)
        self._canvas = Canvas(self, highlightthickness=0)
        self.new_image(name_image)

    def new_image(self, name_image: NameImage):
        if self._canvas.find_withtag(name_image.name):
            self._canvas.delete(name_image.name)
        self._canvas.config(width=name_image.width(), height=name_image.height())
        self._canvas.create_image(name_image.width() / 2, name_image.height() / 2, image=name_image.image)
        self._canvas.pack()
