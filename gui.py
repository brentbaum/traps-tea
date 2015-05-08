from Tkinter import *
import ttk
import tkFileDialog
from main import make_art
from PIL import ImageTk, Image

import random, struct, sys, time, os

root = Tk()

upload_frame = ttk.Frame(root, padding="3 3 12 12")
img_frame = ttk.Frame(root, padding="3 3 12 12")
filename = ""

def get_file():
    global filename
    filename = tkFileDialog.askopenfilename()

n_points = IntVar()
def process_file():
    global filename
    make_art(filename, n_points.get())
    img = ImageTk.PhotoImage(Image.open("out/swapopt.png"))
    print("Finished!")
    panel = ttk.Label(img_frame, image = img)
    panel.grid(column=1, row=2, sticky=(N, W))
    panel.image = img
    upload_frame.grid_remove()
    img_frame.grid()

def setup_upload():
    upload_frame.grid(column=0, row=0, sticky=(N, W, E, S))
    upload_frame.columnconfigure(0, weight=1)
    upload_frame.rowconfigure(0, weight=1)
    
    n_entry = ttk.Entry(upload_frame, width=5, textvariable=n_points)
    
    ttk.Button(upload_frame, text='Choose Image File', command=get_file).grid(row=1, column=1, sticky=(W, E))
    n_entry.grid(column=2, row=1, sticky=(W, E))
    ttk.Button(upload_frame, text="Create TSP Art", command=lambda: process_file()).grid(column=3, row=1, sticky=W)
    
    for child in upload_frame.winfo_children(): child.grid_configure(padx=5, pady=5)

def back():
    upload_frame.grid()
    img_frame.grid_remove()

def setup_img_display():
    img_frame.grid(column=0, row=0, sticky=(N, W, E, S))
    img_frame.columnconfigure(0, weight=1)
    img_frame.rowconfigure(0, weight=1)
    
    ttk.Label(img_frame)
    ttk.Button(img_frame, text="Another Image", command=lambda: back()).grid(column=1, row=3, sticky=W)

    for child in img_frame.winfo_children(): child.grid_configure(padx=5, pady=5)

    img_frame.grid_remove()

def setup():
    root.title("TSP Art")
    setup_upload()
    setup_img_display()

setup()
root.mainloop()
