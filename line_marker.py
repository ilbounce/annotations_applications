import json
import os
import tkinter as tk
from os import listdir
from os.path import isfile, join
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from PIL import ImageTk, Image

IMG_WIDTH = 720
IMG_HEIGHT = 30


def resize_image(image, width, height):
    wpercent = (width/float(image.size[0]))
    hpercent = (height/float(image.size[1]))
    if wpercent < hpercent:
        hsize = int((float(image.size[1])*float(wpercent)))
        image = image.resize((width, hsize), Image.ANTIALIAS)
    else:
        wsize = int((float(image.size[0])*float(hpercent)))
        image = image.resize((wsize, height), Image.ANTIALIAS)
    return image

class bidirectional_iterator(object):
    def __init__(self, collection):
        self.collection = collection
        self.index = -1

    def __next__(self):
        try:
            self.index += 1
            result = self.collection[self.index]
        except IndexError:
            raise StopIteration
        return result

    def prev(self):
        if self.index == 0:
            return self.collection[self.index]
        self.index -= 1
        if self.index < 0:
            raise StopIteration
        return self.collection[self.index]

    def __iter__(self):
        return self

# root = tk.Tk()

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        frame = Frame(self)
        # Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 1, weight=1)
        frame.grid(row=0, column=0, sticky=N + S + E + W)
        grid = Frame(frame)
        grid.grid(sticky=N + S + E + W, column=1, row=1, columnspan=3)
        # Grid.rowconfigure(frame, 1, weight=1)
        Grid.columnconfigure(frame, 1, weight=1)
        self.image = None
        self.l1 = Label(self, text="Разметка текста со строк")
        self.l1.config(font=('helvetica', 14))
        self.l1.grid(row=0, column=0, columnspan=3, pady=10, padx=10)
        Label(self, text="Папка с изображениями:").grid(row=1, column=0, pady=10, padx=10)
        self.image_path_entry = Entry(self)
        self.image_path_entry.grid(row=1, column=1, pady=10, padx=10, sticky=N + S + W + E)
        self.btn_open = Button(self, text="Открыть", command=self._insert_text, bg='brown', fg='white',
                               font=('helvetica', 9, 'bold'))
        self.btn_open.grid(row=1, column=2, pady=10, padx=10)
        self.next_prev_frame = Frame(self)
        self.next_prev_frame.grid(row=2, column=0, pady=0, padx=0)
        self.btn_next = Button(self.next_prev_frame, text="Следующее", command=lambda: self._get_image('next'), bg='brown', fg='white',
                               font=('helvetica', 9, 'bold'), height=1, width=12)
        self.btn_next.grid(row=0, column=0, pady=0, padx=0)
        self.btn_prev = Button(self.next_prev_frame, text="Предыдущее", command=lambda: self._get_image('prev'), bg='brown', fg='white',
                               font=('helvetica', 9, 'bold'), height=1, width=12)
        self.btn_prev.grid(row=1, column=0, pady=2, padx=0)
        self.ignore_processed = IntVar()
        self.ignore_processed.set(1)
        self.cb_ignore_processed = Checkbutton(self, text="Пропускать заполненные",
                                               variable=self.ignore_processed,
                                               onvalue=1, offvalue=0)
        self.cb_ignore_processed.grid(row=2, column=1, pady=10, padx=10, sticky=W)
        self.img_label = Label(self)
        self.img_label.grid(row=2, column=1, pady=10, padx=10)
        self.img_file_label = Label(self)
        self.img_file_label.grid(row=2, column=2, pady=10, padx=10)
        Label(self, text="Введите текст с изображения:").grid(row=3, column=0, pady=10, padx=10)
        self.image_text_entry = Entry()
        self.image_text_entry.grid(row=3, column=1, pady=10, padx=10, sticky=N + S + W + E)
        self.btn_save = Button(self, text="Сохранить", command=self._save_markup, bg='brown', fg='white',
                               font=('helvetica', 9, 'bold'))
        self.btn_save.grid(row=3, column=2, pady=10, padx=10)
        self.bind('<Return>', self._save_event)
        self.btn_delete = Button(self, text="Удалить", command=self._delete_image, bg='brown', fg='white',
                               font=('helvetica', 9, 'bold'))
        self.btn_delete.grid(row=4, column=2, pady=10, padx=10)
        self.bind('<Alt-Delete>', self._delete_event)

    def _insert_text(self):
        self.btn_next.config(state=NORMAL)
        dir_name = fd.askdirectory()
        self.image_path_entry.insert(0, dir_name)
        self.image_path = dir_name
        self.img_files_iterator = bidirectional_iterator([f for f in listdir(dir_name) if isfile(join(dir_name, f))])
        self._get_image('next')

    def _get_image(self, direction):
        if not self.image_path:
            mb.showerror(
                "Ошибка",
                "Не задана папка с картинками")
        else:
            if direction == 'next':
                if self.ignore_processed.get() == 1:
                    while True:
                        self.image, filename = self._get_next_image()
                        self.image_filename = filename
                        if not self.image or not self.check_json_file():
                            break
                else:
                    self.image, filename = self._get_next_image()
            else:
                self.image, filename = self._get_prev_image()
            if self.image:
                self.img_label.config(image=self.image)
                self.img_file_label.config(text=filename)
                self.image_filename = filename
                self.image_text_entry.delete(0, 'end')
                self.image_text_entry.insert(0, self.check_json_file())
#                 self.quit()
#                 self.mainloop()
            else:
                self.btn_next.config(state=DISABLED)
        return

    def _get_next_image(self):
        if not self.image_path:
            mb.showerror(
                "Ошибка",
                "Не задана папка с картинками")
        else:
            image_file = next(self.img_files_iterator, None)
            if image_file:
                image = Image.open(os.path.join(self.image_path, image_file))
                image = resize_image(image, IMG_WIDTH, IMG_HEIGHT)
                # image.thumbnail((IMG_WIDTH, IMG_HEIGHT))
                return ImageTk.PhotoImage(image), image_file
            else:
                return None, None
            
    def _get_prev_image(self):
        if not self.image_path:
            mb.showerror(
                "Ошибка",
                "Не задана папка с картинками")
        else:
            image_file = self.img_files_iterator.prev()
            if image_file:
                image = Image.open(os.path.join(self.image_path, image_file))
                image = resize_image(image, IMG_WIDTH, IMG_HEIGHT)
                # image.thumbnail((IMG_WIDTH, IMG_HEIGHT))
                return ImageTk.PhotoImage(image), image_file
            else:
                return None, None

    def _save_event(self, event):
        self._save_markup()

    def _save_markup(self):
        markup_text = self.image_text_entry.get()
        if not markup_text:
            mb.showerror(
                "Ошибка",
                "Не задан текст с картинки")
            return

        markup_path = os.path.join(self.image_path, "markup")
        if not os.path.exists(markup_path):
            try:
                os.mkdir(markup_path)
            except OSError:
                mb.showerror(
                    "Ошибка", "Не удалось создать папку %s " % markup_path)
                return
        image = ImageTk.PhotoImage(Image.open(os.path.join(self.image_path, self.image_filename)))
        result = {
            "files": self.image_filename,
            "text": self.image_text_entry.get(),
            "xmin": 0,
            "ymin": 0,
            "xmax": image.width(),
            "ymax": image.height()
        }
        file_name = os.path.splitext(self.image_filename)[0] + ".json"
        with open(os.path.join(markup_path, file_name), 'w', encoding='utf-8') as file:
            file.write(json.dumps(result, ensure_ascii=False))
        self._get_image('next')

    def _delete_event(self, event):
        self._delete_image()

    def _delete_image(self):
        if self.image_filename:
            os. remove(os.path.join(self.image_path, self.image_filename))
            self._get_image()

    def check_json_file(self):
        file_name = os.path.splitext(self.image_filename)[0] + ".json"
        markup_path = os.path.join(self.image_path, "markup")
        full_path = os.path.join(markup_path, file_name)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as json_file:
                image_dict = json.load(json_file)
                return image_dict["text"]
        return ""


if __name__ == "__main__":
    app = App()
    app.geometry('1500x250')
    app.mainloop()
