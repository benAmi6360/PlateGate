import Camera
import tkinter
import numpy
import cv2
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk


image_name = None
img = None
image_button = None


def upload_file():
    global image_name, img, image_button
    f_types = [('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    image = Image.open(filename)
    resized = image.resize((400, 300))
    selected_image = ImageTk.PhotoImage(resized)
    img = selected_image
    image_button = tkinter.Button(window, image=img)
    image_button.grid(row=2, column=1)
    image_name = filename


def send_file():
    global image_name, image_button, img
    if image_name is None or image_button is None:
        messagebox.askokcancel('Error!', 'No image uploaded')
        return
    cv_image = cv2.imread(image_name)
    client = Camera.Camera('127.0.0.1', 1337, 900164)
    recognized = client.recognize(cv_image)
    if recognized:
        filename = 'recognized.png'
        with open(filename, 'wb') as f:
            f.write(recognized)
        image = Image.open(filename)
        selected_image = ImageTk.PhotoImage(image)
        img = selected_image
        image_button.destroy()
        image_button = tkinter.Button(window, image=img)
        image_button.grid(row=2, column=1)
        image_name = filename
        messagebox.askokcancel('Gate Open', 'The image passed the checks thus the gate will open')
        return
    messagebox.askokcancel('Error!', 'Image didn\'t passed the checks and the gate will not open')


class MainWindow(tkinter.Tk):
    def __init__(self, window_title):
        super().__init__()
        self.title(window_title)
        self.geometry("800x600")
        self.label = tkinter.Label(self, text='PlateGate Image Upload')
        self.label.grid(row=0, column=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.button = tkinter.Button(self, text='Upload Image', command=upload_file)
        self.button.grid(row=1, column=1)
        self.submit = tkinter.Button(self, text='Send image', command=send_file)
        self.submit.grid(row=3, column=1)


window = MainWindow('PlateGate')
window.mainloop()
