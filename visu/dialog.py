from tkinter import Toplevel, Button, CENTER, LEFT, RIGHT, Label, BaseWidget


class Dialog(Toplevel):
    def __init__(self, parent: BaseWidget, text: str):
        super().__init__(parent)
        self.attributes('-topmost', True)
        self.attributes('-toolwindow', True)
        self.deiconify()
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
        self.bind('<FocusOut>', lambda e: self.destroy())


class ConfirmDialog(Dialog):
    def __init__(self, parent: BaseWidget, action=lambda: print('no binding action'),
                 text: str = 'Подтвердить действие?', title: str = 'Подтверждение'):
        super().__init__(parent, text)
        self.title(title)

        text_lab = Label(self, text=self.text)

        def ok_action():
            action()
            self.destroy()

        ok_but = Button(self, text='Да', command=ok_action, width=6)
        cancel_but = Button(self, text='Отмена', command=lambda: self.destroy(), width=6)
        text_lab.pack(anchor=CENTER)
        ok_but.pack(side=LEFT, padx=10)
        cancel_but.pack(side=RIGHT, padx=10)
        self.update()
        width = max(text_lab.winfo_width(), ok_but.winfo_width() + cancel_but.winfo_width() + 40)
        height = text_lab.winfo_height() + ok_but.winfo_height() + 10
        shift_x = int(self.winfo_width() / 2)
        shift_y = int(self.winfo_height() / 2)
        self.geometry(f"{width}x{height}+{parent.winfo_pointerx() - shift_x}+{parent.winfo_pointery() - shift_y}")


class InfoDialog(Dialog):
    INFO = 0
    WARNING = 1
    ERROR = 2

    def __init__(self, parent: BaseWidget, text: str = 'Что-то случилось!', mode: int = INFO):
        super().__init__(parent, text)
        match mode:
            case InfoDialog.WARNING:
                title = 'Предупреждение'
                color = 'orange'
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
        width = max(text_lab.winfo_width(), ok_but.winfo_width() + 20)
        height = text_lab.winfo_height() + ok_but.winfo_height() + 10
        shift_x = int(self.winfo_width() / 2)
        shift_y = int(self.winfo_height() / 2)
        self.geometry(f"{width}x{height}+{parent.winfo_pointerx() - shift_x}+{parent.winfo_pointery() - shift_y}")