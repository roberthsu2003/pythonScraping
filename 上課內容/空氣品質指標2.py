#!/usr/bin/python3
'''
應用程式說明
'''

from tkinter import Tk
import dataSource


class AirWindow(Tk):
    def __init__(self):
        super().__init__()
        #取得資料
        self.airData=dataSource.getAirData()
        if self.airData == None:
            print("下載錯誤")
        else:
           print(self.airData)

        #建立視窗
        self.title("台灣各地空氣品質指標")
        self.geometry('300x100+200+200')
        self.resizable(width=0, height=0)


if __name__ == '__main__':
    window = AirWindow()
    window.mainloop()