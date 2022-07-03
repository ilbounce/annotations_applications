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
        self.box_lst = []
        self.im = None

        self.DIR = 'image_2'

        self.rect = None

        self.start_x = None
        self.start_y = None

        self.fin_x = None
        self.fin_y = None

        self.canvas = None

        self.classes = np.zeros(12)
        self.classes[0] = 1

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

        self.images = glob.glob('test/test/' + self.DIR + '/*')
        self.iterator = -1

        lab = tk.Label(self.frame3, text='boxes:').pack(side='top')

        btn_img = tk.Button(self.frame1, text = 'input new image (q)', width = 15, height = 5, bg='white',fg="black")
        btn_img.bind("<Button-1>", self._draw_image)
        self.bind('q', self._draw_image)
        btn_img.grid(row = 0, column = 0)

        btn_ret = tk.Button(self.frame1, text = 'return (w)', width = 15, height = 5, bg="white",fg="black")
        btn_ret.bind("<Button-1>", self.delete_box_info)
        self.bind('w', self.delete_box_info)
        btn_ret.grid(row = 0, column = 1)

        btn_add = tk.Button(self.frame1, text = 'add box (space)', width = 15, height = 5, bg="white",fg="black")
        btn_add.bind('<Button-1>', self.add_box)
        self.bind('<space>', self.add_box)
        btn_add.grid(row = 0, column = 2)

        btn_re = tk.Button(self.frame1, text = 'change box (e)', width = 15, height = 5, bg="white",fg="black")
        btn_re.bind('<Button-1>', self.destroy_box)
        self.bind('e', self.destroy_box)
        btn_re.grid(row=0, column=3)

        btn_pass = tk.Button(self.frame1, text = 'pass image (r)', width = 15, height = 5, bg="white",fg="black")
        btn_pass.bind('<Button-1>', self.pass_image)
        self.bind('r', self.pass_image)
        btn_pass.grid(row=0, column=4)

        btn_save = tk.Button(self.frame1, text = 'save image (enter)', width = 15, height = 5, bg="white",fg="black")
        btn_save.bind('<Button-1>', self.save_image)
        self.bind('<Return>', self.save_image)
        btn_save.grid(row=1, column=4)

        btn_del = tk.Button(self.frame1, text = 'delete last (s)', width = 15, height = 5, bg="white",fg="black")
        btn_del.bind('<Button-1>', self.delete_info)
        self.bind('s', self.delete_info)
        btn_del.grid(row=2, column=4)

        btn_canc = tk.Button(self.frame1, text = 'cancel pass (d)', width = 15, height = 5, bg="white",fg="black")
        btn_canc.bind('<Button-1>', self.cancel_pass)
        self.bind('d', self.cancel_pass)
        btn_canc.grid(row=3, column=4)

        btn_tshort = tk.Button(self.frame1, command = lambda num = 0: self.class_match(num),
            text = 'T-Short (1)', width = 15, height = 5, bg="white",fg="black")
        btn_tshort.bind("<Button-1>", lambda event, num = 0: self.class_match_event(event, num))
        self.bind('1', lambda event, num = 0: self.class_match_event(event, num))
        btn_tshort.grid(row = 1, column = 0)

        btn_pants = tk.Button(self.frame1, command = lambda num = 1: self.class_match(num),
            text = 'Pants (2)', width = 15, height = 5, bg="white",fg="black")
        btn_pants.bind("<Button-1>", lambda event, num = 1: self.class_match_event(event, num))
        self.bind('2', lambda event, num = 1: self.class_match_event(event, num))
        btn_pants.grid(row = 1, column = 1)

        btn_shorts = tk.Button(self.frame1, command = lambda num = 2: self.class_match(num),
            text = 'Shorts (3)', width = 15, height = 5, bg="white",fg="black")
        btn_shorts.bind("<Button-1>", lambda event, num = 2: self.class_match_event(event, num))
        self.bind('3', lambda event, num = 2: self.class_match_event(event, num))
        btn_shorts.grid(row = 1, column = 2)

        btn_dress = tk.Button(self.frame1, command = lambda num = 3: self.class_match(num),
            text = 'Dress (4)', width = 15, height = 5, bg="white",fg="black")
        btn_dress.bind("<Button-1>", lambda event, num = 3: self.class_match_event(event, num))
        self.bind('4', lambda event, num = 3: self.class_match_event(event, num))
        btn_dress.grid(row = 1, column = 3)

        btn_shoes = tk.Button(self.frame1, command = lambda num = 4: self.class_match(num),
            text = 'Shoes (5)', width = 15, height = 5, bg="white",fg="black")
        btn_shoes.bind("<Button-1>", lambda event, num = 4: self.class_match_event(event, num))
        self.bind('5', lambda event, num = 4: self.class_match_event(event, num))
        btn_shoes.grid(row = 2, column = 0)

        btn_sneakers = tk.Button(self.frame1, command = lambda num = 5: self.class_match(num),
            text = 'Sneakers (6)', width = 15, height = 5, bg="white",fg="black")
        btn_sneakers.bind("<Button-1>", lambda event, num = 5: self.class_match_event(event, num))
        self.bind('6', lambda event, num = 5: self.class_match_event(event, num))
        btn_sneakers.grid(row = 2, column = 1)

        btn_costume = tk.Button(self.frame1, command = lambda num = 6: self.class_match(num),
            text = 'Costume (7)', width = 15, height = 5, bg="white",fg="black")
        btn_costume.bind("<Button-1>", lambda event, num = 6: self.class_match_event(event, num))
        self.bind('7', lambda event, num = 6: self.class_match_event(event, num))
        btn_costume.grid(row = 2, column = 2)

        btn_bag = tk.Button(self.frame1, command = lambda num = 7: self.class_match(num),
            text = 'Bag (8)', width = 15, height = 5, bg="white",fg="black")
        btn_bag.bind("<Button-1>", lambda event, num = 7: self.class_match_event(event, num))
        self.bind('8', lambda event, num = 7: self.class_match_event(event, num))
        btn_bag.grid(row = 2, column = 3)

        btn_hat = tk.Button(self.frame1, command = lambda num = 8: self.class_match(num),
            text = 'Hat (9)', width = 15, height = 5, bg="white",fg="black")
        btn_hat.bind("<Button-1>", lambda event, num = 8: self.class_match_event(event, num))
        self.bind('9', lambda event, num = 8: self.class_match_event(event, num))
        btn_hat.grid(row = 3, column = 0)

        btn_glasses = tk.Button(self.frame1, command = lambda num = 9: self.class_match(num),
            text = 'Glasses (0)', width = 15, height = 5, bg="white",fg="black")
        btn_glasses.bind("<Button-1>", lambda event, num = 9: self.class_match_event(event, num))
        self.bind('0', lambda event, num = 9: self.class_match_event(event, num))
        btn_glasses.grid(row = 3, column = 1)

        btn_hoodie = tk.Button(self.frame1, command = lambda num = 10: self.class_match(num),
            text = 'Hoodie (i)', width = 15, height = 5, bg="white",fg="black")
        btn_hoodie.bind("<Button-1>", lambda event, num = 10: self.class_match_event(event, num))
        self.bind('i', lambda event, num = 10: self.class_match_event(event, num))
        btn_hoodie.grid(row = 3, column = 2)

        btn_shirt = tk.Button(self.frame1, command = lambda num = 11: self.class_match(num),
            text = 'Shirt (o)', width = 15, height = 5, bg="white",fg="black")
        btn_shirt.bind("<Button-1>", lambda event, num = 11: self.class_match_event(event, num))
        self.bind('o', lambda event, num = 11: self.class_match_event(event, num))
        btn_shirt.grid(row = 3, column = 3)



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
        with open('test/bounding_box.pickle', 'rb') as f:
            final_data = pickle.load(f)

        for widget in self.frame4.winfo_children():
            widget.destroy()

        counter = len(final_data)

        count_lab = tk.Label(self.frame4, text = 'Amount of data: ' + str(counter)).pack(side = 'top')
        self.iterator += 1
        self.box_lst = []
        if self.canvas is not None:
            self.canvas.destroy()
        self.im = Image.open(self.images[self.iterator])
        self.im.thumbnail(self.size)
        self.w, self.h = self.im.size
        self.canvas = tk.Canvas(self.frame2, width=self.w, height=self.h, cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)

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
