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
        self.size = 700, 700
        self.im = None

        self.total = 12344

        self.canvas = None

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

        self.images = glob.glob('pictures2/*')
        self.iterator = -1

#         lab = tk.Label(self.frame3, text='boxes:').pack(side='top')

        btn_img = tk.Button(self.frame1, text = 'input new image (q)', width = 15, height = 5, bg='white',fg="black")
        btn_img.bind("<Button-1>", self._draw_image)
        self.bind('q', self._draw_image)
        btn_img.grid(row = 0, column = 0)

        btn_lic = tk.Button(self.frame1, text = 'license (w)', width = 15, height = 5, bg="white",fg="black")
        btn_lic.bind("<Button-1>", self.to_license)
        self.bind('w', self.to_license)
        btn_lic.grid(row = 0, column = 1)

        btn_other = tk.Button(self.frame1, text = 'other (e)', width = 15, height = 5, bg="white",fg="black")
        btn_other.bind('<Button-1>', self.to_other)
        self.bind('e', self.to_other)
        btn_other.grid(row = 0, column = 2)
        
        btn_cancel = tk.Button(self.frame1, text = 'cancel (r)', width = 15, height = 5, bg="white",fg="black")
        btn_cancel.bind('<Button-1>', self.cancel)
        self.bind('r', self.cancel)
        btn_cancel.grid(row = 0, column = 3)
        
    def to_license(self, event):
        self._draw_image(event)
        os.system('move ' + self.images[self.iterator-1] + ' C:\\Users\\ilbou\\license_scan\\data\\license\\')
#         self.images = self.images[1:]
        
    def to_other(self, event):
        self._draw_image(event)
        os.system('move ' + self.images[self.iterator-1] + ' C:\\Users\\ilbou\\license_scan\\data\\other\\')
#         self.images = self.images[1:]
        
    def cancel(self):
        pass



    def class_match_event(self, event, num):
        self.class_match(num)
        for widget in self.frame1.winfo_children():
            widget['fg'] = 'black'
        if 'Button' not in str(event.widget):
            self.frame1.winfo_children()[8 + num]['fg'] = 'red'
        else:
            event.widget['fg'] = 'red'


    def class_match(self, num):
        self.classes = np.zeros(12)
        self.classes[num] = 1

    def destroy_box(self, event):
        self.canvas.delete(self.rect)
        self.rect = None

    def add_box(self, event):
        self.canvas.delete(self.rect)
        self.rect = None
        self.box_lst.append([np.where(self.classes == 1)[0][0],
        self.start_x, self.start_y, self.fin_x, self.fin_y])
        tk.Label(self.frame3, text = str(self.box_lst[-1])).pack(side='top')

    def delete_box_info(self, event):
        if len(self.box_lst) != 0:
            self.box_lst = self.box_lst[:-1]
            self.frame3.winfo_children()[-1].destroy()

    def pass_image(self, event):
        if self.im is not None:
            name = os.path.split(self.images[self.iterator])[1]
            self.im.save('test/passed/' + name)
            os.system('mv ' + self.images[self.iterator] + ' ' + 'test/reserve/passed/' + name)
            for widget in self.frame3.winfo_children()[1:]:
                widget.destroy()
            self._draw_image(event)

    def save_image(self, event):
        if len(self.box_lst) != 0:
            name = os.path.split(self.images[self.iterator])[1]
            with open('test/bounding_box.pickle', 'rb') as f:
                data = pickle.load(f)
            data['test/processed/' + name] = self.box_lst
            with open('test/bounding_box.pickle', 'wb') as f:
                pickle.dump(data, f)
            self.im.save('test/processed/' + name)
            os.system('mv ' + self.images[self.iterator] + ' ' + 'test/reserve/processed/' + name)
            for widget in self.frame3.winfo_children()[1:]:
                widget.destroy()
            self._draw_image(event)

    def delete_info(self, event):
        with open('test/bounding_box.pickle', 'rb') as f:
            data = pickle.load(f)
        if len(data) != 0 and self.iterator > 0:
            self.iterator -= 1
            name = os.path.split(self.images[self.iterator])[1]
            del data['test/processed/' + name]
            with open('test/bounding_box.pickle', 'wb') as f:
                pickle.dump(data, f)
            os.system('mv test/reserve/processed/' + name + ' ' + self.images[self.iterator])
            os.system('rm test/processed/' + name)
            self.iterator -= 1
            for widget in self.frame3.winfo_children()[1:]:
                widget.destroy()
            self._draw_image(event)

    def cancel_pass(self, event):
        if self.iterator > 0:
            self.iterator -= 1
            name = os.path.split(self.images[self.iterator])[1]
            os.system('mv test/reserve/passed/' + name + ' ' + self.images[self.iterator])
            os.system('rm test/passed/' + name)
            self.iterator -= 1
            for widget in self.frame3.winfo_children()[1:]:
                widget.destroy()
            self._draw_image(event)


    def _draw_image(self, event):
#         with open('test/bounding_box.pickle', 'rb') as f:
#             final_data = pickle.load(f)

        for widget in self.frame3.winfo_children():
            widget.destroy()

        counter = len(glob.glob('data/license/*') + glob.glob('data/other/*'))
        lic_num = len(glob.glob('data/license/*'))
        o_num = len(glob.glob('data/other/*'))

        count_lab = tk.Label(self.frame3, text = 'Amount of data: ' + str(counter) + ' / ' + str(self.total)).pack(side = 'top')
        count_l_o = tk.Label(self.frame3, text = 'Amount of licenses: ' + str(lic_num) + ' Amount of others ' + str(o_num)).pack(side = 'bottom')
        self.iterator += 1
        self.img = self.images[self.iterator]
        try:
            if self.canvas is not None:
                self.canvas.destroy()
            self.im = Image.open(self.images[self.iterator])
            self.im.thumbnail(self.size)
            self.w, self.h = self.im.size
            self.canvas = tk.Canvas(self.frame2, width=self.w, height=self.h, cursor="cross")
            self.canvas.pack(side="top", fill="both", expand=True)
    #         self.canvas.bind("<ButtonPress-1>", self.on_button_press)
    #         self.canvas.bind("<B1-Motion>", self.on_move_press)
    #         self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
            self.tk_im = ImageTk.PhotoImage(self.im)
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)
        except:
            self._draw_image(event)

#     def on_button_press(self, event):
#         # save mouse drag start position
#         self.start_x = event.x
#         self.start_y = event.y

#         #one rectangle
#         if not self.rect:
#             self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline = 'red', width = 2)

#     def on_move_press(self, event):
#         curX, curY = (event.x, event.y)

#         # expand rectangle as you drag the mouse
#         self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

#     def on_button_release(self, event):
#         self.fin_x = event.x
#         self.fin_y = event.y
#         # print(np.where(self.classes == 1)[0][0], event.x, event.y, self.start_x, self.start_y)


if __name__ == "__main__":
    app = App()
    app.geometry('1500x1500')
    app.mainloop()
