import tkinter as tk
from PIL import Image, ImageTk

import numpy as np
import glob
import os

class App(tk.Tk):
    IMAGE_DIR = 'C:\\Users\\ilbou\\license_scan\\images\\razmetka\\rows_ivan\\'
    SAVE_DIR = 'C:\\Users\\ilbou\\license_scan\\images\\razmetka\\inputs_ivan\\'
    PASSED_DIR = 'C:\\Users\\ilbou\\license_scan\\images\\razmetka\\passed_ivan\\'
    TARGET_DIR = 'C:\\Users\\ilbou\\license_scan\\images\\razmetka\\targets_ivan\\'
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        self.size = 500, 500
        self.im = None
        
        self.canvas = None
        self.lines = []
        self.line = None
        self.target = np.zeros((500,))

        self.frame1 = tk.Frame(self)
        # frame1.grid(row = 0, column = 0)
        self.frame1.place(x=0, y=0)

        self.frame2 = tk.Frame(self)
        # self.frame2.grid(row=0, column = 2)
        self.frame2.place(x=450, y = 100)

        self.frame3 = tk.Frame(self)
        # self.frame3.grid(row=1, column=0)
        self.frame3.place(x = 0, y = 400)

        self.frame4 = tk.Frame(self)
        self.frame4.pack(side='bottom')

        self.images = glob.glob(self.IMAGE_DIR + '*g')
        
        self.iterator = -1
        
        self.counter = len(glob.glob(self.SAVE_DIR + '*g'))
        
        btn_img = tk.Button(self.frame1, text = 'input new image (q)', width = 15, height = 5, bg='white',fg="black")
        btn_img.bind("<Button-1>", self._draw_image)
        self.bind('q', self._draw_image)
        btn_img.grid(row = 0, column = 0)
        
        btn_save = tk.Button(self.frame1, text = 'save data (s)', width = 15, height = 5, bg='white',fg="black")
        btn_save.bind("<Button-1>", self._save_image)
        self.bind('s', self._save_image)
        btn_save.grid(row = 0, column = 1)
        
        btn_canc_save = tk.Button(self.frame1, text = 'cancel save (r)', width = 15, height = 5, bg='white',fg="black")
        btn_canc_save.bind("<Button-1>", self._cancel_save)
        self.bind('r', self._cancel_save)
        btn_canc_save.grid(row = 0, column = 2)
        
        btn_pass = tk.Button(self.frame1, text = 'pass image (z)', width = 15, height = 5, bg='white',fg="black")
        btn_pass.bind("<Button-1>", self._pass_image)
        self.bind('z', self._pass_image)
        btn_pass.grid(row = 1, column = 0)
        
        btn_canc_pass = tk.Button(self.frame1, text = 'cancel pass (e)', width = 15, height = 5, bg='white',fg="black")
        btn_canc_pass.bind("<Button-1>", self._cancel_pass)
        self.bind('e', self._cancel_pass)
        btn_canc_pass.grid(row = 1, column = 1)
        
        btn_del_line = tk.Button(self.frame1, text = 'delete line (x)', width = 15, height = 5, bg='white',fg="black")
        btn_del_line.bind("<Button-1>", self._delete_line)
        self.bind('x', self._delete_line)
        btn_del_line.grid(row = 1, column = 2)
        
        
    def _save_image(self, event):
        np.save(self.TARGET_DIR + '%s_target.npy' % str(self.counter).zfill(6), self.target)
        os.system('move ' + self.images[self.iterator] + ' ' + self.SAVE_DIR + '%s_sample.jpg' % str(self.counter).zfill(6))
        self.counter += 1
        self._draw_image(event)
        
    def _cancel_save(self, event):
        if self.counter == 0:
            return
        self.counter -= 1
        os.system('move ' + self.SAVE_DIR + '%s_sample.jpg' % str(self.counter).zfill(6) + ' ' + self.IMAGE_DIR)
        os.system('del /f ' + self.TARGET_DIR + '%s_target.npy' % str(self.counter).zfill(6))
        if self.iterator == -1:
            self.images = [self.IMAGE_DIR + '%s_sample.jpg' % str(self.counter).zfill(6)] + glob.glob(self.IMAGE_DIR + '*g')
            self._draw_image(event)
        elif self.iterator == 0:
            self.iterator -= 1
            self.images = [self.IMAGE_DIR + '%s_sample.jpg' % str(self.counter).zfill(6)] + glob.glob(self.IMAGE_DIR + '*g')
            self._draw_image(event)
        else:
            self.iterator -= 2
#             self.images = [self.IMAGE_DIR + '%s_sample.jpg' % str(self.counter).zfill(6)] + glob.glob(self.IMAGE_DIR + '*g')
            self._draw_image(event)
        
    def _pass_image(self, event):
        os.system('move ' + self.images[self.iterator] + ' ' + self.PASSED_DIR)
        self._draw_image(event)
        
    def _cancel_pass(self, event):
        os.system('move ' + self.PASSED_DIR + self.images[self.iterator-1][-18:] + ' ' + self.IMAGE_DIR)
        self.iterator -= 2
        self._draw_image(event)
        
    def _delete_line(self, event):
        if len(self.lines) != 0:
            self.canvas.delete(self.lines[-1][0])
            self.target[self.lines[-1][1]] = 0.
            self.lines = self.lines[:-1]
            self.frame3.winfo_children()[-1].destroy()
        
    def delete_rect_info(self, event):
        if len(self.rects_lst) != 0:
            self.rects_lst = self.rects_lst[:-1]
            self.frame3.winfo_children()[-1].destroy()
        
    def _line_info(self, event):
        tk.Label(self.frame3, text = 'Вы добавили разрез по координате %d' % self.lines[-1][1]).pack(side = 'top')
        
    def pad_image(self, img):
        padding = img[:,0][:,np.newaxis,:]
        bg = padding.repeat(500, axis = 1)
        bg[:,:img.shape[1]] = img
        return bg
        
    def _draw_image(self, event):
#         with open('test/bounding_box.pickle', 'rb') as f:
#             final_data = pickle.load(f)

        for widget in self.frame3.winfo_children():
            widget.destroy()
        for widget in self.frame4.winfo_children():
            widget.destroy()
        empty = tk.Label(self.frame4, text = '').pack(side = 'top')
        empty = tk.Label(self.frame4, text = '').pack(side = 'top')
        count_lab = tk.Label(self.frame4, text = 'Размечено данных: ' + str(self.counter)).pack(side = 'top')
        self.target = np.zeros((500,))

        self.iterator += 1
        self.img = self.images[self.iterator]
        
        self.lines = []
        self.line = None
        try:
            if self.canvas is not None:
                self.canvas.destroy()
            self.im = Image.open(self.images[self.iterator])
            self.im = self.im.resize((round(self.im.size[0]*2), round(self.im.size[1]*2)))
            self.im.thumbnail(self.size)
            self.im = np.array(self.im)
            self.im = Image.fromarray(self.pad_image(self.im))
            self.w, self.h = self.im.size
            self.im_to_show = self.im.resize((round(self.im.size[0]*2), round(self.im.size[1]*2)))
            self.canvas = tk.Canvas(self.frame2, width=self.w*2, height=self.h*2, cursor="xterm")
            self.canvas.pack(side="top", fill="both", expand=True)
            self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
            self.tk_im = ImageTk.PhotoImage(self.im_to_show)
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)
        except:
            self._draw_image(event)

    def on_button_release(self, event):
        self.x_line = event.x
        self.x = int(np.floor(event.x / 2))
        self.line = self.canvas.create_line(self.x_line, 0, self.x_line, self.h*2, fill = 'red')
        self.lines.append([self.line, self.x])
        self.target[self.x] = 1.
        self._line_info(event)
        
        # print(np.where(self.classes == 1)[0][0], event.x, event.y, self.start_x, self.start_y)


if __name__ == "__main__":
    app = App()
    app.geometry('1500x1500')
    app.mainloop()
