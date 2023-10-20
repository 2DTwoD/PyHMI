from PIL import Image, ImageTk


class Dimension:
    def __init__(self, width: int = 0, height: int = 0):
        self.width = width
        self.height = height

    def isZero(self):
        return self.width == 0 or self.height == 0

    def __str__(self):
        return f"width: {self.width}, height: {self.height}"


class NameImage:
    def __init__(self, name: str = "Noname", image_path: str = "None", dimension: Dimension = Dimension(0, 0)):
        self.name = name
        self.image: Image = None
        self._image = Image.open(image_path)
        self.resize(dimension)

    def width(self):
        return self.image.width()

    def height(self):
        return self.image.height()

    def resize(self, dimension: Dimension):
        if not dimension.isZero():
            self._image = self._image.resize((dimension.width, dimension.height))
        self.image = ImageTk.PhotoImage(self._image)


class Coordinate:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return f"Coordinate x: {self.x}, y: {self.y}"


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


class ValueWithChangeFlag:
    def __init__(self, value=0, name="undefined"):
        self._value = value
        self._not_changed = False
        self._name = name

    def __str__(self):
        return str(self._value)

    def get(self):
        return int(self._value)

    def set(self, value):
        if self._value != value:
            self._not_changed = False
            self._value = value

    def is_not_changed(self):
        result = self._not_changed
        self._not_changed = True
        return result

    @property
    def name(self):
        return self._name


class StateColor:
    def __init__(self, no_active: str = 'gray', active: str = 'red'):
        self.no_active = no_active
        self.active = active


class TextFieldPars:
    def __init__(self, numeric: bool = True, width: int = 6, up_lim: float = 100.0, down_lim: float = 0.0, dec_place: int = 2):
        self.width = width
        self.up_lim = up_lim
        self.down_lim = down_lim
        self.dec_place = dec_place
        self.numeric = numeric