import tkinter as tk
from PIL import Image, ImageTk

import numpy as np
import glob
import os
import pickle


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        self.size = 1000, 1000
        self.im = None
        
        self.canvas = None
        self.rect = None
        self.rects_lst = []

        self.frame1 = tk.Frame(self)
        # frame1.grid(row = 0, column = 0)
        self.frame1.place(x=0, y=0)

        self.frame2 = tk.Frame(self)
        # self.frame2.grid(row=0, column = 2)
        self.frame2.place(x=750, y = 0)

        self.frame3 = tk.Frame(self)
        # self.frame3.grid(row=1, column=0)
        self.frame3.place(x = 0, y = 400)

        self.frame4 = tk.Frame(self)
        self.frame4.pack(side='bottom')

        self.images = glob.glob('dataset_generator/py-image-dataset-generator/licenses/*g')
        
        self.iterator = -1
        
        self.counter = len(glob.glob('license_cell/data/*g'))
        
        btn_img = tk.Button(self.frame1, text = 'input new image (q)', width = 15, height = 5, bg='white',fg="black")
        btn_img.bind("<Button-1>", self._draw_image)
        self.bind('q', self._draw_image)
        btn_img.grid(row = 0, column = 0)
        
        btn_save = tk.Button(self.frame1, text = 'save data (s)', width = 15, height = 5, bg='white',fg="black")
        btn_save.bind("<Button-1>", self._save_image)
        self.bind('s', self._save_image)
        btn_save.grid(row = 0, column = 1)
        
        btn_pass = tk.Button(self.frame1, text = 'pass image (z)', width = 15, height = 5, bg='white',fg="black")
        btn_pass.bind("<Button-1>", self._pass_image)
        self.bind('z', self._pass_image)
        btn_pass.grid(row = 0, column = 2)
        
        btn_del_rect = tk.Button(self.frame1, text = 'delete rectangle (x)', width = 15, height = 5, bg='white',fg="black")
        btn_del_rect.bind("<Button-1>", self._delete_rect)
        self.bind('x', self._delete_rect)
        btn_del_rect.grid(row = 1, column = 0)
        
        btn_add = tk.Button(self.frame1, text = 'add rectangle (a)', width = 15, height = 5, bg='white',fg="black")
        btn_add.bind("<Button-1>", self._add_rect)
        self.bind('a', self._add_rect)
        btn_add.grid(row = 1, column = 1)
        
    def _save_image(self, event):
        self.mask = np.zeros((np.array(self.im).shape))
        if len(self.rects_lst) != 0:
            for elm in self.rects_lst:
                self.mask[elm[0]:elm[1], elm[2]:elm[3]] = 1.
        
        self.sample = np.concatenate([np.array(self.im)[np.newaxis,...], self.mask[np.newaxis,...]], axis = 0)
        
        np.save('C:\\Users\\ilbou\\license_scan\\license_cells\\data\\sample_%s'%str(self.counter).zfill(3), self.sample)
        self.counter += 1
        
        os.system('move ' + self.images[self.iterator] + ' C:\\Users\\ilbou\\license_scan\\license_cells\\processed\\')
        
        self._draw_image(event)
        
    def _pass_image(self, event):
        os.system('move ' + self.images[self.iterator] + ' C:\\Users\\ilbou\\license_scan\\license_cells\\passed\\')
        
        self._draw_image(event)
        
    def _delete_rect(self, event):
        self.canvas.delete(self.rect)
        self.delete_rect_info(event)
        self.rect = None
        
    def delete_rect_info(self, event):
        if len(self.rects_lst) != 0:
            self.rects_lst = self.rects_lst[:-1]
            self.frame3.winfo_children()[-1].destroy()
        
    def _add_rect(self, event):
        self.rects_lst.append([self.start_y,self.fin_y, self.start_x,self.fin_x])
        tk.Label(self.frame3, text = str(self.rects_lst[-1])).pack(side = 'top')
        
        
        
    def _draw_image(self, event):
#         with open('test/bounding_box.pickle', 'rb') as f:
#             final_data = pickle.load(f)

        for widget in self.frame3.winfo_children():
            widget.destroy()

        self.iterator += 1
        self.img = self.images[self.iterator]
        
        self.rects_lst = []
        self.rect = None
        try:
            if self.canvas is not None:
                self.canvas.destroy()
            self.im = Image.open(self.images[self.iterator])
            self.im = self.im.resize((round(self.im.size[0]*3), round(self.im.size[1]*3)))
            self.im.thumbnail(self.size)
            self.w, self.h = self.im.size
            self.canvas = tk.Canvas(self.frame2, width=self.w, height=self.h, cursor="cross")
            self.canvas.pack(side="top", fill="both", expand=True)
            self.canvas.bind("<ButtonPress-1>", self.on_button_press)
            self.canvas.bind("<B1-Motion>", self.on_move_press)
            self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
            self.tk_im = ImageTk.PhotoImage(self.im)
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)
        except:
            self._draw_image(event)
        
    

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        #one rectangle
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline = 'red', width = 2)

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        self.fin_x = event.x
        self.fin_y = event.y
        # print(np.where(self.classes == 1)[0][0], event.x, event.y, self.start_x, self.start_y)


if __name__ == "__main__":
    app = App()
    app.geometry('1500x1500')
    app.mainloop()
