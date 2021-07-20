import tkinter as tk
from tkinter import *

if __name__ == '__main__':
    o_win = tk.Tk()
    o_win.wm_title("Test title...")
    s_geometry = '540x440'
    s_frame_bgcolor = '#B0E0E6'

    o_win.geometry(s_geometry)
    o_win.configure(background=s_frame_bgcolor)

    o_label = Label(o_win, text='권대현 바보')
    o_label.pack()
    o_txt = Entry(o_win)
    o_txt.pack()
    o_btn = Button(o_win, text="ok")
    o_btn.pack()
    o_win.mainloop()
