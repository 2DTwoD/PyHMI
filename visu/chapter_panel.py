from tkinter import Frame, BaseWidget, Button, NSEW, Event
import di_conf.container as DI


class ChapterPanel(Frame):
    def __init__(self, parent: BaseWidget):
        _main_pars = DI.Container.main_pars()
        super(ChapterPanel, self).__init__(parent)
        self._sc = DI.Container.screen_creator()
        _chapter_grid_size = _main_pars.get_chapter_grid_size()
        _screen_names = tuple(_main_pars.screens.keys())
        self._button_list = []
        for col in range(_chapter_grid_size.width):
            self.columnconfigure(index=col, weight=1)
        for row in range(_chapter_grid_size.height):
            for col in range(_chapter_grid_size.width):
                num = col + _chapter_grid_size.width * row
                if num + 1 > len(_screen_names):
                    break
                button = Button(self, text=_screen_names[num])
                button.bind("<Button-1>", self.change_screen_action)
                self._button_list.append(button)
                button.grid(row=row, column=col, sticky=NSEW)

    def change_screen_action(self, event: Event):
        self._sc.current_screen = event.widget.cget('text')


