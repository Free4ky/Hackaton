import torch
import os
from PIL import Image
import shutil
import pandas as pd
import tkinter as tk
import TkinterDnD2 as tkdnd
from tkinter import messagebox as messbx, filedialog
import tkinter.ttk as ttk
import sys

application_path = ''

# КЛАСС МОДЕЛИ
'''
Здесь происходит загрузка обученной модели,
её настройка. Реализованы механизмы детекции,
сохранения обработанных фотографий и csv таблицы.
'''
class Detector:
    def __init__(self):
        global application_path
        self.model = torch.hub.load(os.path.join(application_path, 'yolov5'), 'custom',
                                    path=os.path.join(application_path, 'data/last.pt'), force_reload=True,
                                    source='local')
        self.model.conf = 0.15
        self.res_dict = {
            'filename': [],
            'point_x': [],
            'point_y': []
        }

        self.progress = 0

    def detect(self, path, obj):
        images = []
        obj.pgb['maximum'] = len(os.listdir(path))
        for i, image in enumerate(os.listdir(path)):
            obj.pgb['value'] = i
            obj.update()
            img_path = os.path.join(path, image)
            if os.path.isfile(img_path):
                result = self.model(img_path)
                for item in result.xyxy[0]:
                    result.save()

                    item = item.cpu().numpy()
                    self.res_dict['filename'].append(image)
                    self.res_dict['point_x'].append(item[0] + ((item[2] - item[0]) / 2))
                    self.res_dict['point_y'].append(item[1] + ((item[3] - item[1]) / 2))
            self.progress += 1

    def save(self, path):

        cur_path = os.getcwd()
        for address, dirs, files in os.walk(os.path.join(cur_path, 'runs')):
            for name in files:
                os.replace(os.path.join(address, name), os.path.join(path, name))
        shutil.rmtree(os.path.join(cur_path, 'runs'))

        pd.DataFrame.from_dict(self.res_dict).to_csv(os.path.join(path, 'data.csv'))

# ---------------------------------Классы графического интерфейса-------------------------------------------------------
class Footer(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(Footer, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.main_window = parent.parent
        self.button_frame = tk.Frame(self)
        self.b_start = tk.Button(
            self.button_frame,
            text='Запустить',
            command=self.start
        )
        self.b_save = tk.Button(
            self.button_frame,
            text='Сохранить',
            command=self.save
        )

        # PROGRESS BAR

        self.pgb = ttk.Progressbar(
            self,
            orient='horizontal',
            mode='determinate',
            maximum=0,
            value=0
        )
        self.button_frame.pack()
        self.b_start.grid(row=0, column=0, padx=30)
        self.b_save.grid(row=0, column=1, padx=30)
        self.pgb.pack(fill=tk.X, side='bottom', pady=15)

    def list_b_folder(self, event):
        dire = filedialog.askdirectory(title='Выбрать папку для сохранения')
        self.path = dire

    def start(self):
        self.b_start['state'] = 'disabled'

        self.parent.model.detect(self.parent.path, self)

        self.b_start['state'] = 'normal'

    def save(self):
        self.list_b_folder(event=None)
        self.parent.model.save(path=self.path)


class DragAndDrop(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(DragAndDrop, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.mw = self.parent.parent
        self.var = tk.StringVar()
        # FRAMES
        self.entry_frame = tk.Frame(self)
        # LABELS
        tk.Label(self, text='Путь до папки', bg='#BDD6D9').pack(anchor=tk.NW, padx=10)
        # ENTRIES
        self.e_box = tk.Entry(self.entry_frame, textvariable=self.var, width=100)
        # BUTTONS
        self.search = tk.Button(
            self.entry_frame,
            text='Выбрать папку',
            command=self.find_input_folder
        )

        # LABEL FRAME
        self.lframe = tk.LabelFrame(self, text='Инструкция', bg='#BDD6D9')
        tk.Label(
            self.lframe,
            bg='#BDD6D9',
            text='Перетащите папку с фотографиями \nв рамку инструкции.\n Вы получите путь в поле выше.'
        ).pack(fill=tk.BOTH, expand=True)
        self.lframe.drop_target_register(tkdnd.DND_FILES)
        self.lframe.dnd_bind('<<Drop>>', self.drop)
        # PLACING
        self.entry_frame.pack(fill='x')
        self.e_box.pack(fill=tk.X, side=tk.LEFT, padx=10)
        self.search.pack(side=tk.LEFT)
        self.lframe.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def drop(self, event):
        print(event.data)
        x = event.data.lstrip('{')
        x = x.rstrip('}')
        self.var.set(x)
        self.parent.path = self.e_box.get()
        print(self.parent.path)

    def find_input_folder(self):
        dire = filedialog.askdirectory(title='выбрать папку для сохранения')
        self.var.set(dire)
        self.parent.path = dire


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
    MainApplication(root).pack(side="top", fill="both", expand=True, )
    root.mainloop()


if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    start()
