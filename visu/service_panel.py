from tkinter import Frame, Label, BaseWidget, Canvas, LEFT, RIGHT, W
import di_conf.container as DI


class ServicePanel(Frame):
    def __init__(self, parent: BaseWidget):
        super(ServicePanel, self).__init__(parent)

        self._com = DI.Container.communication()
        self.sc = DI.Container.screen_creator()

        self.mx = Label(self, text=0, width=5, anchor=W)
        self.my = Label(self, text=0, width=5, anchor=W)
        self.sc.bind('<Motion>', self._mouse_coordinates_visu)

        self._connect_rect_canvas = Canvas(self, width=20, height=20, highlightthickness=0)
        self._connect_rect = self._connect_rect_canvas.create_rectangle(0, 0, 20, 20, fill='red')
        self.mx.pack(side=LEFT)
        self.my.pack(side=LEFT)
        self._connect_rect_canvas.pack(side=RIGHT)

    def _mouse_coordinates_visu(self, e):
        self.mx.config(text=f'x: {e.x}')
        self.my.config(text=f'y: {e.y}')

    def refresh(self):
        self._connect_rect_canvas.itemconfig(self._connect_rect, fill='green' if self._com.connected else 'red')
