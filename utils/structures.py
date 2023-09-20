from PIL.ImageTk import PhotoImage


class NameImage:
    def __init__(self, name: str = "Noname", image: PhotoImage = "None"):
        self.name = name
        self.image = image

    def width(self):
        return self.image.width()

    def height(self):
        return self.image.height()


class Coordinate:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = int(x)
        self.y = int(y)


class Dimension:
    def __init__(self, width: int = 0, height: int = 0):
        self.width = width
        self.height = height

    def __str__(self):
        return f"width: {self.width}, height: {self.height}"

class Area:
    def __init__(self):
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0

    def update(self, up, down, left, right):
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    def __str__(self):
        return f"up: {self.up}, down: {self.down}, left: {self.left}, right: {self.right}"



class CommPair:
    def __init__(self):
        self._send_flag = False
        self._address = 0
        self._data = [0]

    def new_data(self, address=0, data=None):
        self._address = address
        self._data = [0] if data is None else data
        self._send_flag = True

    @property
    def data_ready(self):
        return self._send_flag

    @property
    def get(self):
        self._send_flag = False
        return {
            "address": self._address,
            "data": self._data
        }


