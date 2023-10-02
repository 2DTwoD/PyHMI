from PIL import ImageTk, Image

from utils.structures import NameImage


class CommonService:
    def __init__(self):
        self.alarm_token = NameImage(name="alarm_token",
                                     image=ImageTk.PhotoImage(Image.open('res/pics/common/alarm.png')))
        self.locked = NameImage(name="locked_token",
                                     image=ImageTk.PhotoImage(Image.open('res/pics/common/locked.png')))
        self.unlocked = NameImage(name="unlocked_token",
                                  image=ImageTk.PhotoImage(Image.open('res/pics/common/unlocked.png')))
