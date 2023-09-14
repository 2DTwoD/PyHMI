from PIL.ImageTk import PhotoImage


class NameImage:
    def __init__(self, name: str = "Noname", image: PhotoImage = "None"):
        self.name = name
        self.image = image


class Coordinate:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y
