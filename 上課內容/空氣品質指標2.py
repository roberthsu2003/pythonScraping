#!/usr/bin/python3
'''
應用程式說明
'''

from tkinter import Tk
class AirWindow(Tk):
    def __init__(self):
        super().__init__()
        pass

if __name__ == '__main__':
    window = AirWindow()
    window.mainloop()