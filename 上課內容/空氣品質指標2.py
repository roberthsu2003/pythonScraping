#!/usr/bin/python3
'''
應用程式說明
'''

from tkinter import Tk
class AirWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("台灣各地空氣品質指標")
        self.geometry('300x100')
        self.resizable(width=0, height=0)


if __name__ == '__main__':
    window = AirWindow()
    window.mainloop()