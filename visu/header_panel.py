from tkinter import Frame, TOP, LEFT, RIGHT

import di_conf.container as DI


class HeaderPanel(Frame):
    def __init__(self):
        self.sc = DI.Container.screen_creator()
        super(HeaderPanel, self).__init__(self.sc.main_frame)
        self.chapter_frame = Frame(self)
        self.adjust_frame = Frame(self)

        self.chapter_frame.pack(side=LEFT)
        self.adjust_frame.pack(side=RIGHT)
