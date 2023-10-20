from tkinter import Toplevel, Button, CENTER, LEFT, RIGHT, Label, BaseWidget


class Dialog(Toplevel):
    def __init__(self, parent: BaseWidget, text: str):
        super(Dialog, self).__init__(parent)
        self.attributes('-topmost', True)
        self.attributes('-toolwindow', True)
        self.focus_set()
        self.resizable(False, False)

        characters_in_line = 40
        count = 0
        words = text.split(' ')
        self.text = ''
        for word in words:
            if len(word) > characters_in_line:
                word = word[0: characters_in_line]
            count += len(word)
            self.text += word
            if count > characters_in_line:
                self.text += '\n'
                count = 0
            else:
                self.text += ' '

        self.text_lab = Label(self, text=text)

    def set_geometry(self, parent):
        width = self.winfo_width()
        height = self.winfo_height()
        shift_x = int(width / 2)
        shift_y = int(height / 2)
        x = parent.winfo_pointerx() - shift_x
        y = parent.winfo_pointery() - shift_y
        x = self._get_limited_var(x, width, 0, self.winfo_screenwidth())
        y = self._get_limited_var(y, height, 0, self.winfo_screenheight())
        self.geometry(f"{width}x{height}+{x}+{y}")

    @staticmethod
    def _get_limited_var(var, var_shift, down_lim, up_lim) -> int:
        if var < down_lim:
            return down_lim
        elif var + var_shift > up_lim:
            return up_lim - var_shift
        return var


class ConfirmDialog(Dialog):
    def __init__(self, parent: BaseWidget, action=lambda: print('no binding action'),
                 text: str = 'Подтвердить действие?', title: str = 'Подтверждение'):
        super(ConfirmDialog, self).__init__(parent, text)
        self.title(title)
        self.bind('<FocusOut>', lambda e: self.destroy())

        text_lab = Label(self, text=self.text)

        def ok_action():
            action()
            try:
                self.destroy()
            except:
                pass

        ok_but = Button(self, text='Да', command=ok_action, width=6)
        cancel_but = Button(self, text='Отмена', command=lambda: self.destroy(), width=6)
        text_lab.pack(anchor=CENTER)
        ok_but.pack(side=LEFT, padx=10)
        cancel_but.pack(side=RIGHT, padx=10)
        self.update()
        self.set_geometry(parent)


class InfoDialog(Dialog):
    INFO = 0
    WARNING = 1
    ERROR = 2

    def __init__(self, parent: BaseWidget, text: str = 'Что-то случилось!', mode: int = INFO):
        super(InfoDialog, self).__init__(parent, text)
        match mode:
            case InfoDialog.WARNING:
                title = 'Предупреждение'
                color = 'orangered3'
            case InfoDialog.ERROR:
                title = 'Ошибка'
                color = 'red'
            case _:
                title = 'Информация'
                color = 'black'
        self.title(title)

        text_lab = Label(self, text=self.text, foreground=color)
        ok_but = Button(self, text='Ок', command=lambda: self.destroy(), width=6)
        text_lab.pack(anchor=CENTER)
        ok_but.pack(anchor=CENTER, padx=10)
        self.update()
        self.set_geometry(parent)
