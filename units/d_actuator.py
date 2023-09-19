from PIL import Image, ImageTk
import di_conf.container as DI
from utils.structures import NameImage, Coordinate, Area, Dimension


class DActuator:
    def __init__(self, name, parameters):
        self.sc = DI.Container.screen_creator()
        self.name = name
        self.stop_img = NameImage(name=self.name + "_stop", image=ImageTk.PhotoImage(Image.open(parameters.img_path.stop)))
        self.start_img = NameImage(name=self.name + "_start", image=ImageTk.PhotoImage(Image.open(parameters.img_path.start)))
        self.alarm_img = NameImage(name=self.name + "_alarm", image=ImageTk.PhotoImage(Image.open(parameters.img_path.alarm)))

        self.location = {}
        for screen_name, location in parameters.location.__dict__.items():
            self.location[screen_name] = Coordinate(location.x, location.y)
        self.width = parameters.dimension.width
        self.height = parameters.dimension.height
        self.current_img = self.stop_img
        print(self.stop_img.width(), self.start_img.width(), self.alarm_img.width())
        self.image_dimension = Dimension(max(self.stop_img.width(), self.start_img.width(), self.alarm_img.width()),
                                         max(self.stop_img.height(), self.start_img.height(), self.alarm_img.height()))
        self.click_area = Area()

    def update(self):

        if self.sc.screen.find_withtag(self.name) == () and self.sc.current_screen in self.location:
            x = self.location[self.sc.current_screen].x
            y = self.location[self.sc.current_screen].y
            self.sc.screen.create_image(x, y, image=self.current_img.image, tag=self.current_img.name)
            self.click_area.update(y - self.image_dimension.height / 2, y + self.image_dimension.height / 2,
                                   x - self.image_dimension.width / 2, x - self.image_dimension.width / 2)

    def click(self, mouse_x, mouse_y):
        if self.click_area.left < mouse_x < self.click_area.right and\
           self.click_area.down < mouse_y < self.click_area.up:
            print("catch up")

