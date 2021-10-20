import sys
import tkinter as tk
from tkinter import *
import sys
from PyQt5.QtWidgets import QApplication, QWidget

class TestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Test App")
        self.move(300, 300)
        self.resize(400, 200)
        self.show()


if __name__ == '__main__':
    """
    o_win = tk.Tk()
    o_win.wm_title("Test title...")
    s_geometry = '540x440'
    s_frame_bgcolor = '#B0E0E6'

    o_win.geometry(s_geometry)
    o_win.configure(background=s_frame_bgcolor)

    o_label = Label(o_win, text='경기도 신봉동 홍천초 4학년 권대현 바보')
    o_label.pack()
    o_txt = Entry(o_win)
    o_txt.pack()
    o_btn = Button(o_win, text="ok")
    o_btn.pack()
    o_win.mainloop()
    """
    o_app = QApplication(sys.argv)
    o_ex = TestApp()
    sys.exit(o_app.exec_())