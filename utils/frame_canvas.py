from tkinter import Frame, Canvas, W

from utils.structures import NameImage


class FrameCanvas(Frame):
    def __init__(self, master, name_image: NameImage):
        super().__init__(master)
        self.canvas = Canvas(self, highlightthickness=0)
        self.new_image(name_image)

    def new_image(self, name_image: NameImage):
        self.canvas.delete("all")
        self.canvas.config(width=name_image.width(), height=name_image.height())
        self.canvas.create_image(name_image.width() / 2, name_image.height() / 2, image=name_image.image)
        self.canvas.pack()
