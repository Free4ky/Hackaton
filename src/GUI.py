import tkinter as tk
import TkinterDnD2 as tkdnd
from model import *


class Head(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(Head, self).__init__(parent, *args, **kwargs)


class Body(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(Body, self).__init__(parent, *args, **kwargs)
        label = tk.Label(self, text='EXAMPLE')
        label.pack()


def set_text(e, text):
    e.delete(0, tk.END)
    e.insert(0, text)
    return


class Footer(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(Footer, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.button_frame = tk.Frame(self)
        self.b_start = tk.Button(
            self.button_frame,
            text='Запустить',
            command=self.start
        )
        self.button_frame.pack()
        self.b_start.pack()

    def start(self):
        self.parent.model.detect(self.parent.path)
        self.parent.model.save()


class DragAndDrop(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(DragAndDrop, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.mw = self.parent.parent
        self.var = tk.StringVar()
        tk.Label(self, text='Путь до папки', bg='#AFEEEE').pack(anchor=tk.NW, padx=10)
        self.e_box = tk.Entry(self, textvariable=self.var, width=80)
        self.e_box.pack(fill=tk.X, padx=10)

        self.lframe = tk.LabelFrame(self, text='Инструкция', bg='#AFEEEE')
        tk.Label(
            self.lframe,
            bg='#AFEEEE',
            text='Перетащите папку с фотографиями \nв рамку инструкции.\n Вы получите путь в поле выше.'
        ).pack(fill=tk.BOTH, expand=True)
        self.lframe.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.lframe.drop_target_register(tkdnd.DND_FILES)
        self.lframe.dnd_bind('<<Drop>>', self.drop)

    def drop(self, event):
        print(event.data)
        x = event.data.lstrip('{')
        x = x.rstrip('}')
        self.var.set(x)
        self.parent.path = self.e_box.get()
        print(self.parent.path)


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.model = Detector()
        self.widgets = {
            'dnd': DragAndDrop(self),
            'footer': Footer(self)
        }

        self.widgets['dnd'].pack(expand=1, fill='both')
        self.widgets['footer'].pack(side='bottom')


HEIGHT = 400
WIDTH = 900


def start():
    root = tkdnd.TkinterDnD.Tk()
    root.geometry(f'{WIDTH}x{HEIGHT}')
    MainApplication(root, background='#BCBCBC').pack(side="top", fill="both", expand=True, )
    root.mainloop()
