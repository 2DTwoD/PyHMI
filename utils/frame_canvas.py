from tkinter import Frame, Canvas, YES, BOTH, NW

from utils.structures import NameImage, Coordinate, Dimension


class FrameCanvas(Frame):
    def __init__(self, parent, name_image: NameImage):
        super(FrameCanvas, self).__init__(parent)
        self._canvas = Canvas(self, width=name_image.width(), height=name_image.height(), highlightthickness=0)
        self._canvas.pack()
        self.images = {}
        self.new_image(name_image)

    def new_image(self, name_image: NameImage, coordinate: Coordinate = Coordinate(0, 0), origin: str = 'nw'):
        if origin not in ('center', 'nw'):
            origin = 'nw'
        if self._canvas.find_withtag(name_image.name) != ():
            self._canvas.delete(name_image.name)
            del self.images[name_image.name]
        self._canvas.create_image(coordinate.x, coordinate.y,
                                  image=name_image.image, tag=name_image.name, anchor=origin)
        self.images[name_image.name] = name_image.image

