from PIL import ImageTk, Image

from utils.structures import NameImage


class CommonService:
    def __init__(self):
        self.alarm_token = NameImage(name="alarm_token",
                                     image_path='res/pics/common/alarm.png')
        self.no_alarm_token = NameImage(name="alarm_token",
                                        image_path='res/pics/common/no_alarm.png')
        self.service_token = NameImage(name="service_token",
                                       image_path='res/pics/common/service.png')
        self.no_service_token = NameImage(name="service_token",
                                          image_path='res/pics/common/no_service.png')
        self.locked_token = NameImage(name="locked_token",
                                      image_path='res/pics/common/locked.png')
        self.unlocked_token = NameImage(name="locked_token",
                                        image_path='res/pics/common/unlocked.png')
