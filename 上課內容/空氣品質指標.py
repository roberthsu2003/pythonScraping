#!/usr/bin/python3.x
'''
這是下載政府開放平台內的資料
使用視窗顯示
'''

from tkinter import *

def createWindow(w):
    print(w)
    print("createWindow")

if __name__ == "__main__":
    window=Tk()
    window.title("空氣品質指標")
    window.geometry("400x150")
    createWindow(window)
    window.mainloop()