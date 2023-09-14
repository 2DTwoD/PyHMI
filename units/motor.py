from PIL import Image, ImageTk
import di_conf.container as DI
from utils.structures import NameImage, Coordinate


class Motor:
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

    def update(self):

        if self.sc.screen.find_withtag(self.name) == () and self.sc.current_screen in self.location:
            self.sc.screen.create_image(self.location[self.sc.current_screen].x,
                                        self.location[self.sc.current_screen].y,
                                        image=self.current_img.image, tag=self.current_img.name)
